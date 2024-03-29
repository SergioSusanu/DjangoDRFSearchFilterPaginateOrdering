from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('category', views.CategoriesView.as_view()),
    path('menu-items', views.MenuItemsView.as_view())
]
