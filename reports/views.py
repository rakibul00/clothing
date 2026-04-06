from django.shortcuts import render
from django.db.models.functions import TruncDay, TruncMonth
from products.models import Product
from django.db.models import Sum, Count, Avg
from sales.models import Sale, SaleItem

def branch_report(request):
    # 1. Main Stats (Cards) - Decimal format fix (|floatformat:2 template e use koro)
    stats = Sale.objects.aggregate(
        total_revenue=Sum('total_price'),
        total_transactions=Count('id'),
        avg_order_value=Avg('total_price')
    )

    # 2. View Type Logic
    view_type = request.GET.get('view', 'daily') 
    
    if view_type == 'monthly':
        report_data = Sale.objects.annotate(period=TruncMonth('date')).values('period', 'branch__name').annotate(
            revenue=Sum('total_price'),
            count=Count('id')
        ).order_by('-period')

    elif view_type == 'branch-wise':
        # ✅ MAMA EI JE FIX: Branch wise filter logic
        report_data = Sale.objects.values('branch__name', 'branch__location').annotate(
            revenue=Sum('total_price'),
            count=Count('id')
        ).order_by('-revenue')

    elif view_type == 'product-wise':
        report_data = SaleItem.objects.values('product__name', 'product__category__name').annotate(
            revenue=Sum('price'),
            count=Sum('quantity')
        ).order_by('-revenue')

    else: # Default Daily
        report_data = Sale.objects.annotate(period=TruncDay('date')).values('period', 'branch__name').annotate(
            revenue=Sum('total_price'),
            count=Count('id')
        ).order_by('-period')

    context = {
        'stats': stats,
        'report_data': report_data,
        'view_type': view_type,
    }
    return render(request, 'reports/report_page.html', context)