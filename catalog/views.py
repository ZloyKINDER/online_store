from django.http.response import HttpResponse
from django.shortcuts import render
from catalog.models import Product, Contact


def home(request):
    products = Product.objects.order_by('-created_at')[:5]
    context = {'products': products}

    return render(request, "home.html", context)


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
    context = {'product': product}

    return render(request, 'catalog/product_detail.html', context)
