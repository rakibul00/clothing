from django.shortcuts import render


def admin_dashboard(request):
    from django.db.models import Sum
    from sales.models import Sale
    from products.models import Product

    # Real data calculation
    revenue = Sale.objects.aggregate(Sum('total_price'))['total_price__sum'] or 0
    sales_count = Sale.objects.count()
    products_count = Product.objects.count()
    returns_count = 0 # Ekhonkar moto 0, pore status field add korle thik hobe

    # Lists
    transactions = Sale.objects.all().order_by('-date')[:5]
    top_products = Product.objects.all()[:2] # Top selling logic pore add kora jabe

    context = {
        'revenue': revenue,
        'sales_count': sales_count,
        'products_count': products_count,
        'returns_count': returns_count,
        'transactions': transactions,
        'top_products': top_products,
    }
    return render(request, 'dashboard.html', context)