from django.shortcuts import render
from products.models import User, Product, Product_group, Type, Cart
from djoser.views import UserViewSet
from rest_framework import mixins, permissions, viewsets
from .permissions import IsAdminOrReadOnly
from .serializers import (ProductGroupSerializer, ProductGroupReadSerializer,
                          TypeSerializer,
                          ProductAddSerializer, ProductReadSerializer,
                          CartSerializer, ProductInCart)



class CustomUserViewSet(UserViewSet):
    '''ViewSet для регистрации пользователя, обновления пароля.'''
    queryset = User.objects.all()
    # permission_classes = (IsAuthenticatedOrReadOnly,)


class Product_groupViewSet(viewsets.ModelViewSet):
    '''
    ViewSet для создания, чтения, редактирования и удаления
    продуктовой категории.
    '''
    queryset = Product_group.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = ProductGroupSerializer

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return ProductGroupReadSerializer
        return ProductGroupSerializer


class TypeViewSet(viewsets.ModelViewSet):
    '''
    ViewSet для создания, чтения, редактирования и удаления
    подкатегории продуктов.
    '''
    queryset = Type.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = TypeSerializer


class ProductViewSet(viewsets.ModelViewSet):
    '''
    ViewSet для создания, чтения, редактирования и удаления
    продуктов.
    '''
    queryset = Product.objects.all()
    permission_classes = (IsAdminOrReadOnly,)


class CartViewSet(viewsets.ModelViewSet):
    '''
    ViewSet для чтения корзины, добавления в нее продуктов, изменения
    и удаления корзины.
    '''
    queryset = Cart.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

