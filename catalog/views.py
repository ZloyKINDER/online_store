from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from catalog.models import Category, Contact, Product


def index(request):
    products = Product.objects.order_by("-created_at")[:8]
    context = {"products": products}
    return render(request, "catalog/index.html", context)


def contacts(request):
    contact = Contact.objects.first()

    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")

        return HttpResponse(
            f"<h1>Спасибо {name}!</h1>"
            f"<h2>Ваше сообщение получено.</h2>"
            f'<p>"{message}"</p>'
            f"<p>С вами свяжутся по этому <b>{phone}</b> номеру.</p>"
        )

    return render(request, "contacts.html", {"contact": contact})


def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    context = {"product": product}

    return render(request, "catalog/product_detail.html", context)


def product_create(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        category_id = request.POST.get("category")
        purchase_price = request.POST.get("purchase_price")
        image = request.FILES.get("image")

        category = get_object_or_404(Category, id=category_id)

        product = Product.objects.create(
            name=name,
            description=description,
            category=category,
            purchase_price=purchase_price,
            image=image,
        )
        context = {"product": product}
        return render(request, "catalog/product_detail.html", context)

    categories = Category.objects.all()
    return render(request, "catalog/product_create.html", {"categories": categories})
