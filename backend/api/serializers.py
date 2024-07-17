from rest_framework.serializers import (CharField, IntegerField,
                                        ModelSerializer, ValidationError)
from shop.models import Category, Product, ShoppingCart, Subcategory


class CategoryGetSerializer(ModelSerializer):
    """GET-Сериализатор модели категории."""
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'image',)


class SubcategoryGetSerializer(ModelSerializer):
    """GET-Сериализатор модели подкатегории."""

    category = CategoryGetSerializer()

    class Meta:
        model = Subcategory
        fields = ('id', 'name', 'slug', 'category', 'image',)


class SubcategorySimpleGetSerializer(ModelSerializer):
    """GET-Сериализатор модели подкатегории, сокращенный. Используется в Сериализаторе модели Корзины."""

    parent_category = CharField(source='category.name')

    class Meta:
        model = Subcategory
        fields = ('id', 'name', 'slug', 'parent_category',)


class ProductGetSerializer(ModelSerializer):
    """GET-Сериализатор модели продукта."""

    subcategory = SubcategorySimpleGetSerializer()

    class Meta:
        model = Product
        fields = ('id', 'name', 'slug', 'price', 'subcategory', 'image_large', 'image_medium', 'image_small',)


class ProductSimpleGetSerializer(ModelSerializer):
    """GET-Сериализатор модели продукта, сокращенный. Используется в Сериализаторе модели Корзины."""

    subcategory = SubcategoryGetSerializer()

    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'subcategory',)


class ShoppingCartGetSerializer(ModelSerializer):
    """GET-Сериализатор модели Корзины."""

    product = CharField(source='product.name')
    price = IntegerField(source='product.price')

    class Meta:
        model = ShoppingCart
        fields = ('product', 'price', 'quantity',)


class ShoppingCartSimpleGetSerializer(ModelSerializer):
    """GET-Сериализатор модели Корзины, сокращенный. Используется в POST-Сериализаторе модели Корзины."""

    class Meta:
        model = ShoppingCart
        fields = ('product', 'quantity',)


class ShoppingCartPostSerializer(ModelSerializer):
    """POST-Сериализатор модели Корзины."""

    products = ShoppingCartSimpleGetSerializer(many=True)

    class Meta:
        model = ShoppingCart
        fields = ('user', 'products',)

    def validate(self, attrs):
        products = attrs.get('products')
        if not products:
            raise ValidationError(
                {
                    "products": [
                        {
                            "product": [
                                "Обязательное поле."
                            ],
                            "quantity": [
                                "Обязательное поле."
                            ]
                        }
                    ]
                }
            )
        products_names: list[str] = []
        for product in products:
            products_names.append(product['product'])
        product_set = set(products_names)
        if len(products) != len(product_set):
            raise ValidationError(
                {
                    "products": [
                        {
                            "product": [
                                "Такой продукт уже добавлен в корзину."
                            ]
                        }
                    ]
                }
            )
        return super().validate(attrs)

    def create(self, validated_data):
        """
        cart_items: list[ShoppingCart] = []
        for item in validated_data['products']:
            cart_items.append(
                ShoppingCart(
                    user=validated_data['user'],
                    product=item['product'],
                    quantity=item['quantity'],
                )
            )
        """
        cart_items = [
            ShoppingCart(
                user=validated_data['user'],
                product=item['product'],
                quantity=item['quantity']
            )
            for item in validated_data['products']
        ]
        objects: list[ShoppingCart] = ShoppingCart.objects.bulk_create(cart_items)
        self.context['objects'] = objects
        return objects

    def to_representation(self, instance):
        objects: list[ShoppingCart] = self.context['objects']
        total_products = len(objects)
        total_price = sum(object.product.price * object.quantity for object in objects)
        products: list[dict[str, any]] = []
        for object in objects:
            products.append(
                {
                    'product': object.product.name,
                    'price': object.product.price,
                    'quantity': object.quantity,
                }
            )
        data = {
            'total_products': total_products,
            'total_price': total_price,
            'products': products,
        }
        return data
