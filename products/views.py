from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category
from django.db.models import Sum
def product_list(request):
    # 🔹 URL theke ID nitechi, tai variable name category_id dile subidha
    category_id = request.GET.get('category') 
    categories = Category.objects.all()

    products = Product.objects.all()

    if category_id:
        # ✅ FIX: category__slug er bodle category_id ba category__id use koro
        products = products.filter(category_id=category_id)

    # 🔥 annotate stock from Inventory
    products = products.annotate(
        stock=Sum('inventory__stock')
    )

    return render(request, 'products/product_list.html', {
        'products': products,
        'categories': categories,
        'selected_category': category_id # Variable name update
    })

def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect('product_list')