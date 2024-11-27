from django.urls import include, path
from rest_framework.routers import DefaultRouter as Router

from .views import (CartViewSet, CustomUserViewSet, ProductGroupViewSet,
                    ProductViewSet, TypeViewSet)

router_v1 = Router()
router_v1.register('users', CustomUserViewSet, basename='user')
router_v1.register('groups', ProductGroupViewSet, basename='group')
router_v1.register('types', TypeViewSet, basename='type')
router_v1.register('products', ProductViewSet, basename='product')
router_v1.register('cart', CartViewSet, basename='cart')


urlpatterns = [
    path('', include(router_v1.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
