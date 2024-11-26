from django.contrib import admin
from .models import Cart, Product, Product_group, Type, CartProduct, ProductImage
from store.constans import MIN_NUM, EMPTY_VALUE

class CartProductInline(admin.TabularInline):
    model = CartProduct
    autocomplete_fields = ('product',)
    extra = MIN_NUM
    min_num = MIN_NUM
    readonly_fields = ('product_price', 'total_price')
    fields = ('product', 'amount', 'product_price', 'total_price')
    
    @admin.display(description='Цена за 1 шт')
    def product_price(self, obj):
        return obj.product.price
    
    @admin.display(description='Итоговая цена')
    def total_price(self, obj):
        return self.product_price(obj)*obj.amount


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3
    min_num = 3
    max_num = 3


class TypeInline(admin.TabularInline):
    model = Type
    extra = MIN_NUM
    min_num = MIN_NUM


@admin.register(Product_group)
class Product_groupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'image')
    search_fields = ('name', 'slug')
    empty_value_display = EMPTY_VALUE
    inlines = (TypeInline,)


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug',
                    'product_group', 'image')
    search_fields = ('name', 'product_group__name')
    list_filter = ('product_group',)
    empty_value_display = EMPTY_VALUE


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'product_group', 'type',
                    'slug', 'price', 'in_stock')
    search_fields = ('name', 'slug')
    list_filter = ('type__product_group', 'type')
    inlines = (ProductImageInline,)
    empty_value_display = EMPTY_VALUE
    
    @admin.display(description='Категория')
    def product_group(self, obj):
        '''Отображает категорию в списке продуктов.'''
        return obj.product_group.name


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    inlines = (CartProductInline,)
    list_display = ('id', 'user', 'display_products',
                    'total_amount', 'total_price')
    search_fields = ('user__username',)
    empty_value_display = EMPTY_VALUE

    @admin.display(description='Продукты')
    def display_products(self, cart):
        return ', '.join([product.name for product in cart.products.all()])
    
    @admin.display(description='Итоговая стоимость')
    def total_price(self, cart):
        return sum(item.amount * item.product.price for item in cart.cartproduct_set.all())
    
    @admin.display(description='Количество товаров в корзине')
    def total_amount(self, cart):
        return sum(item.amount for item in cart.cartproduct_set.all())

    


