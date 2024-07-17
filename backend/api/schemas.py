from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers, status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer

from api.serializers import ShoppingCartGetSerializer

DEFAULT_400_REQUIRED: str = 'Обязательное поле.'
DEFAULT_401: str = 'Учетные данные не были предоставлены.'
DEFAULT_404: str = 'Страница не найдена.'


class ShoppingCartListSerializer(serializers.Serializer):

    total_products = serializers.IntegerField()
    total_price = serializers.IntegerField()
    products = ShoppingCartGetSerializer

    class Meta:
        fields = ('total_products', 'total_price', 'products',)


CATEGORIES_VIEW_SCHEMA: dict = {
    'list': extend_schema(
        description='Получение списка категорий товаров.',
        summary='Получить список категорий товаров.',),
    'retrieve': extend_schema(
        description='Получение категории товаров по id.',
        summary='Получить категорию товара по id.',
    ),
}

PRODUCT_VIEW_SCHEMA: dict = {
    'list': extend_schema(
        description='Получение списка товаров.',
        summary='Получить список товаров.',
    ),
    'retrieve': extend_schema(
        description='Получение товара по slug.',
        summary='Получить товар по slug.',
    ),
}

SHOPPING_CART_SCHEMA = {
    'list': extend_schema(
        description='Получение списка товаров в корзине.',
        summary='Получить список товаров в корзине.',
        responses={
            status.HTTP_200_OK: inline_serializer(
                name='shopping_cart_get_200',
                fields={
                    'total_products': serializers.IntegerField(),
                    'total_price': serializers.IntegerField(),
                    'products': ShoppingCartGetSerializer()},
            ),
            status.HTTP_401_UNAUTHORIZED: inline_serializer(
                name='clear_shopping_cart_error_401',
                fields={'detail': serializers.CharField(default=DEFAULT_401)},
            ),
        },
    ),
    'create': extend_schema(
        description='Обновление списка товаров в корзине.',
        summary='Обновить список товаров в корзине.',
        request=inline_serializer(
            name='shopping_cart_create_201',
            fields={
                'products': ShoppingCartGetSerializer(),
            },
        ),
        responses={
            status.HTTP_201_CREATED: inline_serializer(
                name='shopping_cart_created_201',
                fields={
                    'total_products': serializers.IntegerField(),
                    'total_price': serializers.IntegerField(),
                    'products': ShoppingCartGetSerializer(),},
            ),
            status.HTTP_401_UNAUTHORIZED: inline_serializer(
                name='clear_shopping_cart_error_401',
                fields={
                    'detail': serializers.CharField(default=DEFAULT_401),
                },
            ),
        },
    ),
    'clear_shopping_cart': extend_schema(
        description='Очищает список товаров в корзине.',
        summary='Очистить список товаров в корзине.',
        request=None,
        responses={
            status.HTTP_204_NO_CONTENT: inline_serializer(
                name='clear_shopping_cart_response_204',
                fields={},
            ),
            status.HTTP_401_UNAUTHORIZED: inline_serializer(
                name='clear_shopping_cart_error_401',
                fields={
                    'detail': serializers.CharField(default=DEFAULT_401),
                },
            ),
        },
    ),
}

SUBCATEGORIES_VIEW_SCHEMA: dict = {
    'list': extend_schema(
        description='Получение списка подкатегорий товаров.',
        summary='Получить список подкатегорий.',
    ),
    'retrieve': extend_schema(
        description='Получение подкатегории по id.',
        summary='Получить подкатегорию по id.',
    ),
}

TOKEN_JWT_OBTAIN_SCHEMA: dict = {
    'description': 'Принимает учетные данные пользователя и возвращает JWT токены доступа и обновления.',
    'summary': 'Получить пару JWT токенов для пользователя.',
    'responses': {
        status.HTTP_200_OK: TokenObtainPairSerializer,
        status.HTTP_400_BAD_REQUEST: inline_serializer(
            name='token_create_pair_error_400',
            fields={
                'detail': serializers.CharField(default='No account found with the given credentials',),
            },
        ),
    }
}

TOKEN_JWT_REFRESH_SCHEMA: dict = {
    'description': 'Принимает JWT токен обновления и возвращает JWT токен доступа, если он действителен.',
    'summary': 'Обновить JWT токен доступа.',
    'responses': {
        status.HTTP_200_OK: TokenRefreshSerializer,
        status.HTTP_400_BAD_REQUEST: inline_serializer(
            name='access_token_refresh_error_400',
            fields={
                'detail': serializers.CharField(default='Token is invalid or expired'),
                'code': serializers.CharField(default='token_not_valid')
            },
        ),
    },
}
