from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import contacts, index, product_create, product_detail

app_name = CatalogConfig.name

urlpatterns = [
    path("", index, name="index"),
    path("contacts/", contacts, name="contacts"),
    path("product_detail/<int:product_id>/", product_detail, name="product_detail"),
    path("product_create/", product_create, name="product_create"),
]
