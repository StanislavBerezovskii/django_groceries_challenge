from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from api.schemas import (CATEGORIES_VIEW_SCHEMA, PRODUCT_VIEW_SCHEMA,
                         SHOPPING_CART_SCHEMA, SUBCATEGORIES_VIEW_SCHEMA,
                         TOKEN_JWT_OBTAIN_SCHEMA, TOKEN_JWT_REFRESH_SCHEMA)
from api.serializers import (CategoryGetSerializer, ProductGetSerializer,
                             ShoppingCartGetSerializer,
                             ShoppingCartPostSerializer,
                             SubcategoryGetSerializer)
from shop.models import Category, Product, ShoppingCart, Subcategory


@extend_schema(**TOKEN_JWT_OBTAIN_SCHEMA)
class CustomTokenObtainPairView(TokenObtainPairView):
    """Используется для обновления документации swagger к эндпоинту получения токенов."""
    pass


@extend_schema(**TOKEN_JWT_REFRESH_SCHEMA)
class CustomTokenRefreshView(TokenRefreshView):
    """Используется для обновления документации swagger к эндпоинту обновления токена доступа."""
    pass


@extend_schema_view(**CATEGORIES_VIEW_SCHEMA)
class CategoryViewSet(ModelViewSet):
    """Вьюсет для работы с моделью категории."""

    http_method_names = ('get',)
    serializer_class = CategoryGetSerializer
    queryset = Category.objects.all()


@extend_schema_view(**PRODUCT_VIEW_SCHEMA)
class ProductViewSet(ModelViewSet):
    """Вьюсет для работы с моделью товара."""

    http_method_names = ('get',)
    serializer_class = ProductGetSerializer
    queryset = Product.objects.all().select_related('subcategory')


@extend_schema_view(**SHOPPING_CART_SCHEMA)
class ShoppingCartViewSet(ModelViewSet):
    """Вьюсет для работы с моделью корзины."""

    http_method_names = ('get', 'post',)
    permission_classes = (IsAuthenticated,)
    pagination_class = None

    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user).select_related('user', 'product')

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ShoppingCartGetSerializer
        return ShoppingCartPostSerializer

    @extend_schema(exclude=True)
    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        data: dict[str, any] = serializer.data
        total_products: int = len(data)
        total_price: int = sum(item.get('price', 0) * item.get('quantity', 0) for item in data)
        return Response(
            data={
                'total_products': total_products,
                'total_price': total_price,
                'products': data,
            },
            status=status.HTTP_200_OK
        )

    def create(self, request, *args, **kwargs):
        data: dict[str, any] = request.data
        data['user'] = self.request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ShoppingCart.objects.filter(user=self.request.user).delete()
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    @action(methods=('post',), detail=False, url_name='clear-shopping-cart',)
    def clear_shopping_cart(self, request):
        """Очищает корзину товаров пользователя."""
        ShoppingCart.objects.filter(user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema_view(**SUBCATEGORIES_VIEW_SCHEMA)
class SubcategoryViewSet(ModelViewSet):
    """Вьюсет для работы с моделью подкатегории."""

    http_method_names = ('get',)
    serializer_class = SubcategoryGetSerializer
    queryset = Subcategory.objects.all().select_related('category')
