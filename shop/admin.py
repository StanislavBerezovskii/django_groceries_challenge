from django.contrib import admin

from backend.backend.settings import ADMIN_PAGINATION
from shop.models import Category, Product, ShoppingCart, Subcategory


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Настраивает управление категориями в панели администратора."""
    # Отображение
    list_display = ('id', 'name', 'slug', 'image',)
    # Редактирование
    list_editable = ('name', 'slug', 'image',)
    # Поиск
    search_fields = ('name', 'slug',)
    # Пагинация
    list_per_page = ADMIN_PAGINATION


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Настраивает управление продуктами в панели администратора."""
    # Отображение
    list_display = ('id', 'name', 'slug', 'price', 'subcategory', 'image',)
    # Редактирование
    list_editable = ('name', 'slug', 'price', 'subcategory', 'image',)
    # Поиск
    search_fields = ('name', 'slug', 'price',)
    # Фильтрация
    list_filter = ('subcategory',)
    # Пагинация
    list_per_page = ADMIN_PAGINATION


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    """Настраивает управление корзиной в панели администратора."""
    # Отображение
    list_display = ('id', 'user', 'product', 'quantity',)
    # Редактирование
    list_editable = ('user', 'product', 'quantity',)
    # Поиск
    search_fields = ('user', 'product',)
    # Фильтрация
    list_filter = ('user', 'product')
    # Пагинация
    list_per_page = ADMIN_PAGINATION


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    """Настраивает управление подкатегориями в панели администратора."""
    # Отображение
    list_display = ('id', 'name', 'slug', 'image', 'category',)
    # Редактирование
    list_editable = ('name', 'slug', 'image', 'category',)
    # Поиск
    search_fields = ('name', 'slug',)
    # Фильтрация
    list_filter = ('category',)
    # Пагинация
    list_per_page = ADMIN_PAGINATION
