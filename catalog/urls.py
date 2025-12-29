from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import ContactView, CatalogListViews, CatalogDetailViews, ProductCreateView

app_name = CatalogConfig.name

urlpatterns = [
    path("", CatalogListViews.as_view(), name="product_list"),
    path("contacts/", ContactView.as_view(), name="contacts"),
    path("product_detail/<int:pk>/", CatalogDetailViews.as_view(), name="product_detail"),
    path("product_create/", ProductCreateView.as_view(), name="product_create"),
]
