from django.urls import include, path
from rest_framework.routers import DefaultRouter as Router

# from .views import (CustomUserViewSet, IngredientViewSet, RecipeViewSet,
#                     TagViewSet)

router_v1 = Router()
# router_v1.register('groups', TagViewSet, basename='group')
# router_v1.register('types', RecipeViewSet, basename='type')
# router_v1.register('products', IngredientViewSet, basename='product')


urlpatterns = [
    path('', include(router_v1.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
