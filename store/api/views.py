from django.db import transaction
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .permissions import IsAdminOrReadOnly
from .serializers import (CartSerializer, ProductAddSerializer,
                          ProductGroupReadSerializer, ProductGroupSerializer,
                          ProductInCartSerializer, ProductReadSerializer,
                          TypeSerializer)
from products.models import (Cart, CartProduct, Product, ProductGroup, Type,
                             User)


class CustomUserViewSet(UserViewSet):
    '''ViewSet для регистрации пользователя, обновления пароля.'''
    queryset = User.objects.all()


class ProductGroupViewSet(viewsets.ModelViewSet):
    '''
    ViewSet для создания, чтения, редактирования и удаления
    продуктовой категории.
    '''
    queryset = ProductGroup.objects.all()
    permission_classes = (IsAdminOrReadOnly,)

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

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return ProductReadSerializer
        return ProductAddSerializer


class CartViewSet(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    '''
    ViewSet для чтения корзины, добавления в нее продуктов, изменения
    и удаления корзины.
    '''
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CartSerializer
    pagination_class = None
    http_method_names = ['get', 'post', 'delete', 'patch']

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.action in ['create', 'update', 'partial_update']:
            context['cart'] = Cart.objects.get_or_create(
                user=self.request.user)[0]
        return context

    def create(self, request, *args, **kwargs):
        '''Добавление товара в корзину.'''
        serializer = ProductInCartSerializer(
            data=request.data,
            context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': 'Товар добавлен в корзину.'},
                        status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['delete'], url_path='remove-product')
    def remove_product(self, request):
        '''
        Удаление одного товара из корзины.
        '''
        user = request.user
        product_name = request.data.get('product', None)

        if not product_name:
            return Response({'error': 'Необходимо указать имя товара.'},
                            status=status.HTTP_400_BAD_REQUEST)

        product = get_object_or_404(Product, name=product_name)
        cart = get_object_or_404(Cart, user=user)
        cart_product = get_object_or_404(CartProduct,
                                         cart=cart,
                                         product=product)

        with transaction.atomic():
            product.in_stock += cart_product.amount
            cart_product.delete()
            product.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['delete'], url_path='clear-cart')
    def clear_cart(self, request):
        '''
        Очистка всей корзины.
        '''
        user = request.user
        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            return Response('Ваша корзина уже пустая.',
                            status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            for cart_product in cart.cartproduct_set.all():
                cart_product.product.in_stock += cart_product.amount
                cart_product.product.save()
            cart.delete()

        return Response('Корзина очищена.', status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['patch'], url_path='update-product')
    def update_product(self, request):
        '''
        Обновление количества товара в корзине.
        '''
        user = request.user
        product_name = request.data.get('product', None)
        new_amount = request.data.get('amount', None)

        if not product_name or not new_amount:
            return Response(
                'Необходимо указать название продукта и новое количество.',
                status=status.HTTP_400_BAD_REQUEST
            )

        cart = get_object_or_404(Cart, user=user)
        cart_product = get_object_or_404(
            CartProduct, cart=cart, product__name=product_name)

        product = cart_product.product

        diff = new_amount - cart_product.amount
        if diff > product.in_stock:
            return Response(
                f'Недостаточно товара на складе. '
                f'Доступно: {product.in_stock}.',
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            cart_product.amount = new_amount
            cart_product.save()

            product.in_stock -= diff
            product.save()

        return Response(
            f'Количество товара {product_name} обновлено до {new_amount}.',
            status=status.HTTP_200_OK
        )
