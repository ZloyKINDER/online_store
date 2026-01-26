from django.urls import path

from blog.apps import BlogConfig
from blog.views import BlogCreateView, BlogDeleteViews, BlogDetailViews, BlogListViews, BlogUpdateViews

app_name = BlogConfig.name

urlpatterns = [
    path("", BlogListViews.as_view(), name="blog_list"),
    path("blog_create/", BlogCreateView.as_view(), name="blog_create"),
    path("blog_detail/<int:pk>/", BlogDetailViews.as_view(), name="blog_detail"),
    path("blog/<int:pk>/update", BlogUpdateViews.as_view(), name="blog_update"),
    path("blog/<int:pk>/delete", BlogDeleteViews.as_view(), name="blog_delete"),
]
