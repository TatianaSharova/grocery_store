from products.models import User, Product, Product_group, Type, Cart, CartProduct, ProductImage
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


class TypeSerializer(serializers.ModelSerializer):
    '''Serializer для добавления, редактирования, чтения
    и удаления подкатегории продуктов.'''
    image = Base64ImageField()
    product_group = serializers.PrimaryKeyRelatedField(
        queryset=Product_group.objects.all())
    
    class Meta:
        model = Type
        fields = (
            'id', 'name', 'slug', 'image', 'product_group'
        )


class TypeSmallSerializer(serializers.ModelSerializer):
    '''Serializer для чтения списка подкатегории продуктов
    в каждой категории.'''
    
    class Meta:
        model = Type
        fields = (
            'id', 'name', 'slug', 'image'
        )


class ProductGroupReadSerializer(serializers.ModelSerializer):
    '''Serializer для чтения продуктовой категории.'''
    types = TypeSmallSerializer(many=True, read_only=True,
                                source='type_set')

    class Meta:
        model = Product_group
        fields = (
            'id', 'name', 'slug', 'image', 'types'
        )


class ProductGroupSerializer(serializers.ModelSerializer):
    '''Serializer для добавления, редактирования
    и удаления продуктовой категории.'''
    image = Base64ImageField()

    class Meta:
        model = Product_group
        fields = (
            'id', 'name', 'slug', 'image'
        )
    
    def to_representation(self, instance):
        return ProductGroupReadSerializer(
            instance, context={'request': self.context.get('request')}
        ).data


class ProductImageSerializer(serializers.ModelSerializer):
    '''Сериализатор для изображений продукта.'''

    class Meta:
        model = ProductImage
        fields = ['id', 'image']


class ProductImageAddSerializer(serializers.ModelSerializer):
    '''Сериализатор для изображений продукта.'''
    image = Base64ImageField()
    class Meta:
        model = ProductImage
        fields = ['image',]


class ProductAddSerializer(serializers.ModelSerializer):
    '''Serializer для добавления и редактирования продуктов.'''
    images = ProductImageAddSerializer(many=True, write_only=True)
    type = SlugRelatedField(slug_field='name',
                            queryset=Type.objects.all(),
                            write_only=True)

    class Meta:
        model = Product
        fields = (
            'name', 'slug', 'images',
            'type', 'price', 'in_stock'
        )
    
    def to_representation(self, instance):
        return ProductReadSerializer(
            instance, context={'request': self.context.get('request')}
        ).data
    
    def create(self, validated_data):
        images_data = validated_data.pop('images')
        product = Product.objects.create(**validated_data)
        for image_data in images_data:
            ProductImage.objects.create(product=product, **image_data)
        return product


class ProductReadSerializer(serializers.ModelSerializer):
    '''Serializer для чтения продуктов.'''
    images = ProductImageSerializer(many=True, read_only=True)
    type = SlugRelatedField(slug_field='name',
                            read_only=True)
    product_group = serializers.ReadOnlyField(source='type.product_group.name')
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'name', 'slug', 'type', 'product_group', 'price',
            'images', 'in_stock', 'is_in_shopping_cart'
        )
    
    def get_is_in_shopping_cart(self, obj):
        '''Находится ли продукт в корзине.'''
        user = self.context.get('request').user
        if not user.is_anonymous:
            return CartProduct.objects.filter(cart__user=user, product=obj).exists()
        return False
    
    def to_representation(self, instance):
        '''Удаляет поле is_in_shopping_cart для анонимных пользователей.'''
        representation = super().to_representation(instance)
        user = self.context.get('request').user
        if user.is_anonymous:
            representation.pop('is_in_shopping_cart', None)
        return representation


class ProductInCart(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='product.name')

    class Meta:
        model = CartProduct
        fields = ('name', 'amount')



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


