from django.shortcuts import render
from products.models import User, Product, Product_group, Type, Cart, UserProduct



class CustomUserViewSet(UserViewSet):
    '''
    ViewSet для регистрации пользователя, обновления пароля,
    просмотра профиля пользователя по эндпоинту '/me',
    оформления подписок.
    '''
    queryset = User.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
