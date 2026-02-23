from django.core.cache import cache
from catalog.models import Product


def get_products_by_category(category_id):
    """
    Сервисная функция для получения продуктов в указанной категории
    """
    cache_key = f'category_products_{category_id}'
    products = cache.get(cache_key)

    if not products:
        products = Product.objects.filter(
            category_id=category_id
        ).select_related('category').order_by('-created_at')
        cache.set(cache_key, products, 60 * 15)

    return products


def clear_category_cache(category_id):
    """Очистка кеша для категории"""
    cache_key = f'category_products_{category_id}'
    cache.delete(cache_key)