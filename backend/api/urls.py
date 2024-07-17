from django.urls import include, path
from drf_spectacular.views import (SpectacularAPIView, SpectacularRedocView,
                                   SpectacularSwaggerView)
from rest_framework.routers import DefaultRouter
from rest_framework.viewsets import ModelViewSet

from api.views import (CategoryViewSet, CustomTokenObtainPairView,
                       CustomTokenRefreshView, ProductViewSet,
                       ShoppingCartViewSet, SubcategoryViewSet)

router = DefaultRouter()

ROUTER_DATA: list[dict[str, ModelViewSet]] = [
    {'prefix': 'categories', 'viewset': CategoryViewSet},
    {'prefix': 'products', 'viewset': ProductViewSet},
    {'prefix': 'shopping_cart', 'viewset': ShoppingCartViewSet},
    {'prefix': 'subcategories', 'viewset': SubcategoryViewSet},
]

for route in ROUTER_DATA:
    router.register(
        prefix=route.get('prefix'),
        viewset=route.get('viewset'),
        basename=route.get('prefix')
    )

urlpatterns_docs = [
    path('', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(), name='redoc'),
]

urlpatterns_token = [
    path('create/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns = [
    path('', include(router.urls)),
    path('docs/', include(urlpatterns_docs)),
    path('auth/token/', include(urlpatterns_token)),
]
