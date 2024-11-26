from datetime import datetime, timedelta

import pytest
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient
from products.models import (User, Product, Product_group, Type,
                                   Cart, CartProduct, ProductImage)
from rest_framework.authtoken.models import Token

USERNAME = 'Пользователь'
PASSWORD = 'difficultpass'
EMAIL = 'test@mail.com'
IMAGE = 'data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAMCAgMCAgMDAwMEAwMEBQgFBQQEBQoHBwYIDAoMDAsKCwsNDhIQDQ4RDgsLEBYQERMUFRUVDA8XGBYUGBIUFRT/2wBDAQMEBAUEBQkFBQkUDQsNFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBT/wAARCAADAAMDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD8uyx9aKKKgs//2Q=='
NAME = 'Название'
SLUG = 'slug'
PRICE = 1
AMOUNT = 1
IN_STOCK = 1



# @pytest.fixture
# def user():
#     return User.objects.create_user(username=USERNAME,
#                                     password=PASSWORD,
#                                     email=EMAIL)


@pytest.fixture
def product_group():
    return Product_group.objects.create(name=NAME, slug=SLUG, image=IMAGE)

# @pytest.fixture
# def token(user):
#     """Создаем токен для пользователя."""
#     return Token.objects.create(user=user)

# @pytest.fixture
# def client(token):
#     """Создаем клиента для тестирования API."""
#     client = APIClient()
#     client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
#     return client

@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username=USERNAME,
                                            password=PASSWORD,
                                            email=EMAIL)

@pytest.fixture
def author_client(author):
    client = APIClient()
    token, _ = Token.objects.get_or_create(user=author)
    client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
    return client

@pytest.fixture
def type(product_group):
    return Type.objects.create(name=NAME, slug=SLUG, image=IMAGE,
                               product_group=product_group)

@pytest.fixture
def product(type):
    return Product.objects.create(name=NAME, slug=SLUG, type=type,
                                  price=PRICE, in_stock=IN_STOCK)

@pytest.fixture
def product_images(product):
    for i in range(3):
        ProductImage.objects.create(product=product, image=IMAGE)
    return ProductImage.objects.all()

@pytest.fixture
def cart(author):
    return Cart.objects.create(user=author)

@pytest.fixture
def cart_product(cart, product):
    return CartProduct.objects.create(cart=cart, product=product, amount=AMOUNT)
