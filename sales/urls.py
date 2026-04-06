from django.urls import path
from . import views

urlpatterns = [
    path('pos/', views.pos_view, name='pos'),
    path('complete-sale/', views.complete_sale, name='complete_sale'),
    path('invoice/<int:sale_id>/', views.GenerateInvoice.as_view(), name='generate_invoice'),
    path('search-products/', views.search_products, name='search_products'),
]