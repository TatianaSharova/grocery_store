import pytest
from products.models import (User, Product, Product_group, Type,
                                   Cart, CartProduct, ProductImage)
from conftest import AMOUNT
from http import HTTPStatus

def test_add_product_to_cart(author_client, product, cart):
    '''Тестируем добавление товара в корзину.'''

    data = {
        'product': product.name,
        'amount': AMOUNT
    }
    response = author_client.post('/api/cart/', data=data)

    assert response.status_code == HTTPStatus.CREATED
    cart_product = CartProduct.objects.get(cart=cart, product=product)
    assert cart_product.amount == AMOUNT

def test_clear_cart(author_client, product, cart):
    '''Тестируем очистку корзины.'''

    data = {
        'product': product.name,
        'amount': AMOUNT
    }
    response = author_client.post('/api/cart/', data=data)

    response = author_client.delete('/api/cart/clear-cart/')

    assert response.status_code == HTTPStatus.NO_CONTENT


@pytest.mark.django_db
def test_anonymous_user_cant_add_product_to_cart(
    client, product
):
    '''Анонимный пользователь не может отправить комментарий.'''
    data = {
        'product': product.name,
        'amount': product.in_stock
    }
    response = client.post('/api/cart/', data=data)

    assert response.status_code == HTTPStatus.UNAUTHORIZED


@pytest.mark.django_db
def test_anonymous_user_can_read_product_groups(
    client, product_group, type
):
    '''Анонимный пользователь может получить список продуктовых групп.'''

    response = client.get('/api/groups/')
    assert response.status_code == HTTPStatus.OK

    response = response.json()
    assert 'results' in response

@pytest.mark.django_db
def test_anonymous_user_can_read_product(
    client, product_group, type, product
):
    '''Аноним может просматривать продукты.'''
    response = client.get('/api/products/')
    assert response.status_code == HTTPStatus.OK

    