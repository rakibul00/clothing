import json
import datetime
from branches.models import Branch
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.db.models import Q, Sum
from .models import Sale, SaleItem
from products.models import Product
from django.utils import timezone
from branches.models import Branch # Nishchit koro eita import kora ase
# 1. POS View & Dashboard Statistics
def pos_view(request):
    products_queryset = Product.objects.all()
    products_list = []
    for p in products_queryset:
        products_list.append({
            'id': p.id,
            'name': p.name,
            'price': float(p.price) if p.price else 0.0,
            'code': p.code,
            'image': p.image.url if p.image else ''
        })
    
    # 🔹 ERROR FIX: '-created_at' er bodle '-id' ba '-date' use koro
    # Tumar model choice onujayi eikhane '-date' use kora holo
    recent_sales = Sale.objects.all().order_by('-date')[:10] 
    
    # Dashboard metrics
    total_revenue = Sale.objects.aggregate(total=Sum('total_price'))['total'] or 0
    total_sales_count = Sale.objects.count()

    context = {
        'products_json': json.dumps(products_list),
        'total_revenue': total_revenue,
        'total_sales_count': total_sales_count,
        'recent_sales': recent_sales,
        'quick_sell_id': request.session.pop('quick_sell_id', None)
    }
    return render(request, 'sales/pos.html', context)

# 2. Quick Sell Function (Fixes AttributeError)
def quick_sell(request, product_id):
    request.session['quick_sell_id'] = product_id
    # Tumar urls.py-te pos page-er name jodi 'pos' hoy, tobe nicher line thik ase
    return redirect('pos') 

# 3. Search Products (HTMX ba AJAX-er jonno)
def search_products(request):
    query = request.GET.get('search', '')
    if query:
        products = Product.objects.filter(Q(code__icontains=query) | Q(name__icontains=query))
    else:
        products = Product.objects.all()
    return render(request, 'sales/product_list_results.html', {'products': products})

# 4. Complete Sale Logic (Bulletproof against NoneType Errors)



# 1. POS View & Dashboard Statistics
def pos_view(request):
    products_queryset = Product.objects.all()
    products_list = []
    for p in products_queryset:
        products_list.append({
            'id': p.id,
            'name': p.name,
            'price': float(p.price) if p.price else 0.0,
            'code': p.code,
            'image': p.image.url if p.image else ''
        })
    
    # Recent sales order by date
    recent_sales = Sale.objects.all().order_by('-date')[:10] 
    
    # Dashboard metrics
    total_revenue = Sale.objects.aggregate(total=Sum('total_price'))['total'] or 0
    total_sales_count = Sale.objects.count()

    context = {
        'products_json': json.dumps(products_list),
        'total_revenue': total_revenue,
        'total_sales_count': total_sales_count,
        'recent_sales': recent_sales,
        'quick_sell_id': request.session.pop('quick_sell_id', None)
    }
    return render(request, 'sales/pos.html', context)

# 2. Quick Sell Function
def quick_sell(request, product_id):
    request.session['quick_sell_id'] = product_id
    return redirect('pos') 

# 3. Search Products
def search_products(request):
    query = request.GET.get('search', '')
    if query:
        products = Product.objects.filter(Q(code__icontains=query) | Q(name__icontains=query))
    else:
        products = Product.objects.all()
    return render(request, 'sales/product_list_results.html', {'products': products})

# 4. Complete Sale Logic (Fixed SaleItem Field Error)
def complete_sale(request):
    if request.method == "POST":
        try:
            # Data gathering
            customer_name = request.POST.get('customer_name', 'Guest')
            customer_phone = request.POST.get('customer_phone', '')
            customer_location = request.POST.get('customer_location', '')
            payment_method = request.POST.get('payment_method', 'Cash')
            
            # Safe Price conversion
            raw_total = request.POST.get('total_price') or request.POST.get('total_amount') or 0
            total_price = float(raw_total)

            items_json = request.POST.get('items')
            if not items_json:
                return JsonResponse({'status': 'error', 'message': 'Cart is empty!'}, status=400)
            
            items = json.loads(items_json)
            invoice_no = f"INV-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"

            # Branch Handling
            branch_obj = Branch.objects.first()
            if not branch_obj:
                branch_obj = Branch.objects.create(name="Main Branch", location="Default")

            # ১. Sale Master Record create
            sale = Sale.objects.create(
                invoice_no=invoice_no,
                customer_name=customer_name,
                customer_phone=customer_phone,
                customer_location=customer_location,
                payment_method=payment_method,
                total_price=total_price,
                branch=branch_obj,
                date=timezone.now()
            )

            # ২. Sale Items Save & Stock update
            for item in items:
                try:
                    product_obj = Product.objects.get(id=item['id'])
                    
                    # SaleItem create (Using 'product' object)
                    SaleItem.objects.create(
                        sale=sale,
                        product=product_obj, 
                        quantity=int(item['qty']),
                        price=float(item['price'])
                    )
                    
                    # 🔹 STOCK UPDATE FIX (Auto-detect field name)
                    if hasattr(product_obj, 'stock'):
                        if product_obj.stock is not None:
                            product_obj.stock -= int(item['qty'])
                            product_obj.save()
                    elif hasattr(product_obj, 'quantity'): # Jodi field nam 'quantity' hoy
                        if product_obj.quantity is not None:
                            product_obj.quantity -= int(item['qty'])
                            product_obj.save()
                    else:
                        # Jodi kono field e na pay tobe print hobe terminal e
                        print(f"Warning: Product {product_obj.name} has no stock/quantity field.")
                        
                except Product.DoesNotExist:
                    continue

            return JsonResponse({
                'status': 'success', 
                'message': 'Sale Completed Successfully!',
                'invoice_no': invoice_no,
                'sale_id': sale.id
            })

        except Exception as e:
            print(f"Server Error: {str(e)}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method!'}, status=400)


# 5. Generate Invoice View

class GenerateInvoice(View):
    def get(self, request, sale_id, *args, **kwargs):
        # 1. Sale Master Record get kora
        sale = get_object_or_404(Sale, id=sale_id)
        
        # 2. Sale er under-e shob items (Products) gulo nite hobe
        # select_related use kora bhalo jate product name fast load hoy
        items = SaleItem.objects.filter(sale=sale).select_related('product')
        
        # 3. Calculation Logic (Optional - Jodi model-e field thake tobe sheita use hobe)
        # Amra ekhane calculation kore context-e pathachhi jate HTML-e shubidha hoy
        subtotal = sum(item.price * item.quantity for item in items)
        
        # Vat ar Discount (Jodi model-e thake tobe sale.discount, naile 0 default)
        discount = getattr(sale, 'discount', 0) 
        vat = getattr(sale, 'vat', 0)
        
        # Total Payable
        grand_total = float(subtotal) - float(discount) + float(vat)

        context = {
            'sale': sale,
            'items': items,
            'subtotal': subtotal,
            'discount': discount,
            'vat': vat,
            'grand_total': grand_total,
        }
        return render(request, 'sales/invoice.html', context)