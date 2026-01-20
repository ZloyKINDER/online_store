from django.urls import path

from blog.apps import BlogConfig
from blog.views import BlogListViews, BlogCreateView, BlogDetailViews

app_name = BlogConfig.name

urlpatterns = [
    path("", BlogListViews.as_view(), name="blog_list"),
    path("blog_create/", BlogCreateView.as_view(), name="blog_create"),
    path("blog_detail/<int:pk>/", BlogDetailViews.as_view(), name="blog_detail"),
]
