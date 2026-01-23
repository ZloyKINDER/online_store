from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView

from blog.models import Blog


class BlogListViews(ListView):
    model = Blog

    def get_queryset(self):
        filtered = Blog.objects.filter(is_published=True)
        filtered = filtered.order_by("-created_at")
        return filtered


class BlogCreateView(CreateView):
    model = Blog
    fields = ["title", "content", "preview", "is_published"]
    template_name = "blog/blog_create.html"
    success_url = reverse_lazy("blog:blog_list")


class BlogDetailViews(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.views_count += 1
        obj.save(update_fields=["views_count"])
        return obj


class BlogUpdateViews(UpdateView):
    model = Blog
    fields = ["title", "content", "preview", "is_published"]
    template_name = "blog/blog_create.html"

    def get_success_url(self):
        return reverse_lazy("blog:blog_detail", kwargs={"pk": self.object.pk})


class BlogDeleteViews(DeleteView):
    model = Blog
    success_url = reverse_lazy("blog:blog_list")
