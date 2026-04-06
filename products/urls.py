from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('delete/<int:pk>/', views.delete_product, name='delete_product'),
]