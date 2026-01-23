from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, TemplateView

from catalog.models import Category, Contact, Product


class CatalogListViews(ListView):
    model = Product
    queryset = Product.objects.order_by("-created_at")[:8]


class ContactView(TemplateView):
    template_name = "contacts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["contact"] = Contact.objects.first()
        return context

    def post(self, request, *args, **kwargs):
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")

        return HttpResponse(
            f"<h1>Спасибо {name}!</h1>"
            f"<h2>Ваше сообщение получено.</h2>"
            f'<p>"{message}"</p>'
            f"<p>С вами свяжутся по этому <b>{phone}</b> номеру.</p>"
        )


class CatalogDetailViews(DetailView):
    model = Product


class ProductCreateView(CreateView):
    model = Product
    fields = ["name", "description", "category", "purchase_price", "image"]
    template_name = "catalog/product_create.html"
    success_url = reverse_lazy("catalog:product_list")
