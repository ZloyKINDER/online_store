from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import contacts, home, product_detail

app_name = CatalogConfig.name

urlpatterns = [
    path("", home, name="home"),
    path("contacts/", contacts, name="contacts"),
    path("product_detail/<int:product_id>", product_detail, name="product_detail"),
]
