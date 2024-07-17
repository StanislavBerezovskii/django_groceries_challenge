from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models

from backend.settings import (NAME_MAX_LEN, SHOPPING_CART_MIN_QUANTITY,
                              SLUG_MAX_LEN, set_category_image_name,
                              set_product_image_name_l,
                              set_product_image_name_m,
                              set_product_image_name_s,
                              set_subcategory_image_name)


class Category(models.Model):
    """Модель категории товаров."""

    name = models.CharField(verbose_name='Названиe',
                            max_length=NAME_MAX_LEN,
                            unique=True)
    slug = models.SlugField(verbose_name='URL',
                            max_length=SLUG_MAX_LEN,
                            unique=True)
    image = models.ImageField(verbose_name='Изображение',
                              upload_to=set_category_image_name,
                              # TODO: REMOVE ON RELEASE
                              blank=True,
                              null=True,)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория товаров'
        verbose_name_plural = 'Категории товаров'

    def __str__(self):
        return f'{self.name}'


class Subcategory(models.Model):
    """Модель подкатегории товаров."""

    name = models.CharField(verbose_name='Названиe',
                            max_length=NAME_MAX_LEN,
                            unique=True,)
    slug = models.SlugField(verbose_name='URL',
                            max_length=SLUG_MAX_LEN,
                            unique=True,)
    image = models.ImageField(verbose_name='Изображение',
                              upload_to=set_subcategory_image_name,
                              # TODO: REMOVE ON RELEASE
                              blank=True,
                              null=True,)
    category = models.ForeignKey(verbose_name='Категория',
                                 to=Category,
                                 related_name='subcategories',
                                 on_delete=models.PROTECT,)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Подкатегория товаров'
        verbose_name_plural = 'Подкатегории товаров'

    def __str__(self):
        return f'{self.name} ({self.category.name})'


class Product(models.Model):
    """Модель продукта."""

    name = models.CharField(verbose_name='Названиe',
                            max_length=NAME_MAX_LEN,
                            unique=True,)
    slug = models.SlugField(verbose_name='URL',
                            max_length=SLUG_MAX_LEN,
                            unique=True,)
    price = models.DecimalField(verbose_name='Цена',
                                max_digits=10,
                                decimal_places=2,
                                validators=[MinValueValidator(0)])
    subcategory = models.ForeignKey(verbose_name='Подкатегория',
                                    to=Subcategory,
                                    related_name='products',
                                    on_delete=models.PROTECT,)
    image_large = models.ImageField(verbose_name='Изображение',
                                    upload_to=set_product_image_name_l,
                                    # TODO: REMOVE ON RELEASE
                                    blank=True,
                                    null=True,)
    image_medium = models.ImageField(verbose_name='Изображение',
                                     upload_to=set_product_image_name_m,
                                     # TODO: REMOVE ON RELEASE
                                     blank=True,
                                     null=True,)
    image_small = models.ImageField(verbose_name='Изображение',
                                    upload_to=set_product_image_name_s,
                                    # TODO: REMOVE ON RELEASE
                                    blank=True,
                                    null=True,)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return f'{self.name} ({self.price})'


class ShoppingCart(models.Model):
    """Модель товара в корзине. Связывает товары с пользователями."""

    user = models.ForeignKey(verbose_name='Пользователь',
                             to=User,
                             related_name='shopping_cart',
                             on_delete=models.CASCADE,)
    product = models.ForeignKey(verbose_name='Товар',
                                to=Product,
                                related_name='shopping_cart',
                                on_delete=models.CASCADE,)
    quantity = models.PositiveIntegerField(verbose_name='Количество',
                                           validators=[MinValueValidator(
                                               limit_value=SHOPPING_CART_MIN_QUANTITY,
                                               message='В корзину не были добавлены товары!',
                                           )],)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'product'),
                name='unique_user_product',
            ),
        ]
        ordering = ('id',)
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзинах'

    def __str__(self):
        return f'{self.user}: ({self.product.name}) ({self.quantity})'
