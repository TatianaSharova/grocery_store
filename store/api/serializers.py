from products.models import User, Product, Product_group, Type, Cart, CartProduct
import base64

from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from rest_framework.relations import SlugRelatedField
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import exceptions, serializers
from rest_framework.validators import UniqueTogetherValidator


class UserCreationSerializer(UserCreateSerializer):
    '''Serializer для создания пользователя.'''

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'password',
        )


class Base64ImageField(serializers.ImageField):
    '''Кодировка изображения.'''
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class ProductGroupSerializer(serializers.ModelSerializer):
    '''Serializer для добавления, редактирования
    и удаления продуктовой категории.'''
    image = Base64ImageField()

    class Meta:
        model = Product_group
        fields = (
            'id', 'name', 'slug', 'image'
        )


class ProductGroupReadSerializer(serializers.ModelSerializer):
    '''Serializer для чтения  продуктовой категории.'''

    class Meta:
        model = Product_group
        fields = (
            'id', 'name', 'slug', 'image'
        )


class TypeSerializer(ProductGroupSerializer):
    '''Serializer для добавления, редактирования, чтения
    и удаления подкатегории продуктов.'''
    product_group = serializers.PrimaryKeyRelatedField(
        queryset=Product_group.objects.all())
    
    class Meta:
        model = Type
        fields = (
            'id', 'name', 'slug', 'image', 'product_group'
        )


class ProductAddSerializer(serializers.ModelSerializer):
    '''Serializer для добавления и редактирования продуктов.'''
    image = Base64ImageField()
    type = serializers.PrimaryKeyRelatedField(
        queryset=Type.objects.all())
    # product_group = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'id', 'name', 'slug', 'image',
            'type'
        )


class ProductReadSerializer(serializers.ModelSerializer):
    '''Serializer для чтения продуктов.'''
    type = serializers.PrimaryKeyRelatedField(
        queryset=Type.objects.all())
    product_group = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'id', 'name', 'slug', 'image',
            'type', 'product_group', 'is_in_shopping_cart'
        )
    
    def get_product_group(self, obj):
        '''Определяет к какой категории продуктов относится.'''
        return self.type.product_group
    
    def get_is_in_shopping_cart(self, obj):
        '''Находится ли продукт в корзине.'''
        user = self.context.get('request').user
        if not user.is_anonymous:
            return CartProduct.objects.filter(user=user, product=obj).exists()
        return False


class ProductInCart(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='product.id')
    name = serializers.ReadOnlyField(source='product.name')

    class Meta:
        model = CartProduct
        fields = ('id', 'name', 'amount')



class CartSerializer(serializers.ModelSerializer):
    user = SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    products = ProductInCart()

    class Meta:
        model = Cart
        fields = (
            'id', 'products'
        )


