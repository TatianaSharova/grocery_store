from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from store.constans import (MAX_LENGTH, MIN_NUM,
                            MIN_NUM_IN_STOCK)

User = get_user_model()

class Product_group(models.Model):
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
        verbose_name = 'Группа продуктов'
        verbose_name_plural = 'Группы продуктов'
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
    product_group = models.ForeignKey(Product_group,
                                      on_delete=models.CASCADE,
                                      verbose_name='группа продуктов')
    
    class Meta:
        verbose_name = 'Тип'
        verbose_name_plural = 'Типы'
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
                             verbose_name='Тип')
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


class ProductImage(models.Model):
    '''Модель для изображений продукта.'''
    product = models.ForeignKey(
        'Product', on_delete=models.CASCADE, related_name='images', verbose_name='Продукт'
    )
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


    
