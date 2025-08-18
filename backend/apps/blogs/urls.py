from django.urls import path
from . import views

urlBlogs = [
    path('news/', views.blog_safira, name='news'),
]