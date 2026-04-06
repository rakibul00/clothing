from django.db import models
from branches.models import Branch
from products.models import Product

# 1. Main Sale Model
class Sale(models.Model):
    STATUS_CHOICES = [('Completed', 'Completed'), ('Pending', 'Pending'), ('Refunded', 'Refunded')]
    
    invoice_no = models.CharField(max_length=50, unique=True) 
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=100, blank=True, null=True) 
    customer_phone = models.CharField(max_length=15, blank=True, null=True) 
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0) # Eita check koro    payment_method = models.CharField(max_length=50, default='Bkash') 
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Completed')
    date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50)
    customer_location = models.CharField(max_length=255, blank=True, null=True)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    vat = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payable_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.invoice_no

# 2. Sale Item Model (Protita product er details)
class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, related_name='saleitem', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def subtotal(self):
        # Auto calculate price * quantity
        return self.price * self.quantity

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"