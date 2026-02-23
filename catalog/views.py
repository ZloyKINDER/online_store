from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView, TemplateView
from django.http import HttpResponse

from catalog.models import Category, Contact, Product
from .forms import CategoryForm, ProductForm

from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.cache import cache

from catalog.services import get_products_by_category



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


class ProductListViews(ListView):
    model = Product
    # queryset = Product.objects.order_by("-created_at")[:8]

    def get_queryset(self):
        queryset = cache.get('product_queryset')
        if not queryset:
            queryset = super().get_queryset()
            cache.set('product_queryset', queryset, 60 * 15)  # Кешируем данные на 15 минут
        return queryset


@method_decorator(cache_page(60 * 15), name='dispatch')
class ProductDetailViews(LoginRequiredMixin, DetailView):
    model = Product


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("catalog:product_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, 'Продукт успешно создан!')
        return super().form_valid(form)


class ProductUpdateViews(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"

    def test_func(self):
        product = self.get_object()
        user = self.request.user

        if product.owner == user:
            return True

        if user.is_superuser:
            return True

        messages.error(self.request, 'Вы не являетесь владельцем этого продукта')
        return False

    def form_valid(self, form):
        if 'is_published' in form.changed_data and not form.instance.is_published:
            if not self.request.user.has_perm('catalog.can_unpublish_product'):
                messages.error(self.request, 'У вас нет прав на отмену публикации')
                return redirect('catalog:product_detail', pk=self.object.pk)

        messages.success(self.request, 'Продукт успешно обновлен!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("catalog:product_detail", kwargs={"pk": self.object.pk})



class ProductDeleteViews(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy("catalog:product_list")

    def test_func(self):
        """Проверка прав на удаление"""
        product = self.get_object()
        user = self.request.user

        if product.owner == user:
            return True

        if user.has_perm('catalog.can_delete_any_product'):
            return True

        if user.is_superuser:
            return True

        messages.error(self.request, 'У вас нет прав на удаление этого продукта')
        return False

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Продукт успешно удален!')
        return super().delete(request, *args, **kwargs)


class CategoryCreateViews(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "catalog/category_form.html"
    success_url = reverse_lazy("catalog:product_list")


class CategoryUpdateViews(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = "catalog/category_form.html"
    success_url = reverse_lazy("catalog:category_list")


class CategoryListViews(ListView):
    model = Category


class CategoryProductListView(ListView):
    model = Product
    template_name = 'catalog/category_products.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        from django.shortcuts import get_object_or_404
        from .services import get_products_by_category

        self.category = get_object_or_404(Category, id=self.kwargs['category_id'])
        return get_products_by_category(self.category.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context