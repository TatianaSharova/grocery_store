from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models

from store.constans import MAX_LENGTH, MIN_NUM, MIN_NUM_IN_STOCK

User = get_user_model()


class ProductGroup(models.Model):
    '''Модель для определения категории.'''
    name = models.CharField('Название', unique=True,
                            max_length=MAX_LENGTH,
                            blank=False)
    slug = models.SlugField('Слаг',
                            max_length=MAX_LENGTH,
                            unique=True)
    image = models.ImageField('Изображение',
                              upload_to='product_group/')

    class Meta:
        verbose_name = 'Категория продуктов'
        verbose_name_plural = 'Категории продуктов'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Type(models.Model):
    '''Модель для определения подкатегории.'''
    name = models.CharField('Название', unique=True,
                            max_length=MAX_LENGTH,
                            blank=False)
    slug = models.SlugField('Слаг',
                            max_length=MAX_LENGTH,
                            unique=True)
    image = models.ImageField('Изображение',
                              upload_to='type/')
    product_group = models.ForeignKey(ProductGroup,
                                      on_delete=models.CASCADE,
                                      verbose_name='Продуктовая категория')

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Product(models.Model):
    '''Модель для определения продукта.'''
    name = models.CharField('Название', max_length=MAX_LENGTH,
                            unique=True, blank=False)
    slug = models.SlugField('Слаг', max_length=MAX_LENGTH,
                            unique=True, blank=False)
    type = models.ForeignKey(Type, on_delete=models.CASCADE,
                             verbose_name='Подкатегория')
    price = models.SmallIntegerField(
        'Цена',
        validators=[
            MinValueValidator(
                MIN_NUM, f'Минимальная цена {MIN_NUM}'),
        ],)
    in_stock = models.SmallIntegerField(
        'Остаток в магазине',
        validators=[
            MinValueValidator(
                MIN_NUM_IN_STOCK,
                f'Минимальное количество {MIN_NUM_IN_STOCK}'),
        ],)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ('name',)

    def __str__(self):
        return f'{self.name}'

    @property
    def product_group(self):
        '''Возвращает категорию продукта через подкатегорию.'''
        return self.type.product_group

    def decrease_stock(self, amount):
        '''Уменьшить остаток на складе.'''
        self.in_stock -= amount
        self.save()

    def increase_stock(self, amount):
        '''Увеличить остаток на складе.'''
        self.in_stock += amount
        self.save()


class ProductImage(models.Model):
    '''Модель для изображений продукта.'''
    product = models.ForeignKey('Product', on_delete=models.CASCADE,
                                related_name='images', verbose_name='Продукт')
    image = models.ImageField('Изображение', upload_to='product/')

    class Meta:
        verbose_name = 'Изображение продукта'
        verbose_name_plural = 'Изображения продуктов'
        ordering = ('product',)

    def __str__(self):
        return f'{self.product.name} - {self.image}'


class Cart(models.Model):
    '''Модель для определения продуктовой корзины.'''
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='Пользователь')
    products = models.ManyToManyField(Product, through='CartProduct',
                                      verbose_name='Содержание корзины')

    class Meta:
        verbose_name = 'Корзина пользователя'
        verbose_name_plural = 'Корзины пользователей'
        ordering = ('user',)

    def __str__(self):
        return f'Содержание корзины пользователя {self.user}.'


class CartProduct(models.Model):
    '''Модель для добавления продуктов в корзину.'''
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,
                             verbose_name='Корзина')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                verbose_name='Содержание корзины')
    amount = models.SmallIntegerField(
        'Количество',
        validators=[
            MinValueValidator(
                MIN_NUM, f'Минимальное количество {MIN_NUM}'),
        ],)

    class Meta:
        verbose_name = 'Продукт в корзине'
        verbose_name_plural = 'Продукты в корзине'
        ordering = ('cart',)
        constraints = [
            models.UniqueConstraint(
                fields=['cart', 'product'],
                name='unique_product_in_cart')]

    def __str__(self):
        return f'В корзину добавили {self.amount} {self.product}.'

    def clean(self):
        '''Проверка наличия достаточного количества товара на складе.'''
        if self.amount > self.product.in_stock:
            raise ValidationError(
                f'Недостаточно товара {self.product.name} на складе. '
                f'Доступно: {self.product.in_stock}.')

    def save(self, *args, **kwargs):
        '''Переопределение сохранения для изменения остатка.'''
        self.full_clean()
        if self.pk is None:
            self.product.decrease_stock(self.amount)
        else:
            original = CartProduct.objects.get(pk=self.pk)
            diff = self.amount - original.amount
            if diff > 0:
                self.product.decrease_stock(diff)
            elif diff < 0:
                self.product.increase_stock(-diff)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        '''Возвращаем остаток при удалении из корзины.'''
        self.product.increase_stock(self.amount)
        super().delete(*args, **kwargs)
