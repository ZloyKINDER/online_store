from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import (ProductDetailViews, ProductListViews, ContactView,
                           ProductCreateView, ProductDeleteViews, ProductUpdateViews,
                           CategoryCreateViews, CategoryUpdateViews, CategoryListViews)

app_name = CatalogConfig.name

urlpatterns = [
    path("", ProductListViews.as_view(), name="product_list"),
    path("contacts/", ContactView.as_view(), name="contacts"),
    path("product_detail/<int:pk>/", ProductDetailViews.as_view(), name="product_detail"),
    path("product_create/", ProductCreateView.as_view(), name="product_create"),
    path("product/<int:pk>/update", ProductUpdateViews.as_view(), name="product_update"),
    path("product/<int:pk>/delete", ProductDeleteViews.as_view(), name="product_delete"),
    path("category_create/", CategoryCreateViews.as_view(), name="category_create"),
    path("category/<int:pk>/update", CategoryUpdateViews.as_view(), name="category_update"),
    path("category/", CategoryListViews.as_view(), name="category_list"),
]
