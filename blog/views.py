from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, TemplateView

from blog.models import Blog

class BlogListViews(ListView):
    model = Blog
    queryset = Blog.objects.order_by("-created_at")[:8]


class BlogCreateView(CreateView):
    model = Blog
    fields = ["title", "content", "preview", "is_published"]
    template_name = "blog/blog_create.html"
    success_url = reverse_lazy("blog:blog_list")

class BlogDetailViews(DetailView):
    model = Blog