from django.contrib import admin
from .models import Product, Category, Inventory


class InventoryInline(admin.TabularInline):
    model = Inventory

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'price', 'quantity', 'branch']
    list_filter = ['branch']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass