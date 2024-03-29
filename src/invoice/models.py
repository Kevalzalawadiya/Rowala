from django.db import models
from django.utils import timezone
from django.db.models import Sum
from django.contrib.auth.models import User


# Create your models here.
class Product(models.Model):
    WARRANTY_CHOICES = (
        ('1 YEAR', '1 YEAR'),
        ('2 YEAR', '2 YEAR'),
        ('No warranties', 'No warranties'),
    )
    product_name = models.CharField(max_length=255)
    product_price = models.FloatField(default=0)
    product_unit = models.CharField(max_length=255, null=True, blank=True)
    product_is_delete = models.BooleanField(default=False)
    product_warranty = models.CharField(choices=WARRANTY_CHOICES, null=True,
                                        blank=True, max_length=20, default='No warranties')

    def __str__(self):
        return str(self.product_name)


class Subscription(models.Model):
    months = models.IntegerField()
    service_period = models.IntegerField(help_text='Enter number of mounth in which you want to give services.')

    def __str__(self):
        return f"Repert Service after {self.service_period}-{self.service_period} month for {self.months}-months "


class Invoice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField()
    customer = models.CharField(default='', max_length=255)
    contact = models.CharField(
        max_length=255, default='', blank=True, null=True) # Address field
    email = models.EmailField(default='', blank=True, null=True)
    phone_number = models.BigIntegerField(blank=True, null=True) 
    alt_phone_number = models.BigIntegerField(blank=True, null=True) 
    total = models.FloatField(default=0)
    subscription = models.ForeignKey(
        Subscription, on_delete=models.SET_NULL, blank=True, null=True
    )
    is_bank_account = models.BooleanField(default=False, null=True, blank=True)
    
    def __str__(self):
        return str(f'{self.id} {self.customer} {self.phone_number}')
    
    @property
    def get_total_bill(self):
        invoices = self.invoice.all()
        total = 0
        for invoice in invoices:
            total += float(invoice.product.product_price) * float(invoice.amount)
        return total
    
    @property
    def get_total_services(self):
        return self.total_service.count()
    

class InvoiceDetail(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    invoice = models.ForeignKey(
        Invoice, on_delete=models.SET_NULL, blank=True, null=True, related_name='invoice')
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.IntegerField(default=1)

    @property
    def get_total_bill(self):
        total = float(self.product.product_price) * float(self.amount)
        return total
    
    @classmethod
    def total_income(cls):
        total_income = cls.objects.aggregate(total=Sum(models.F('product__product_price') * models.F('amount')))['total'] or 0
        return total_income


class Service(models.Model):
    invoice = models.ForeignKey(
        Invoice, on_delete=models.CASCADE, blank=True, null=True, related_name='total_service')
    service_date = models.DateField()
    generate_date = models.DateField(auto_now_add=True)
    complate_date = models.DateField()
    is_complate = models.BooleanField(default=False)
    service_number = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.service_date} {self.is_complate}"
    
    
class Complain(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE,  null=True, blank=True)
    created_date = models.DateField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)
    description = models.TextField()

    def __str__(self):
        return f'{self.invoice} {self.id}'
    

class BankAccount(models.Model):
    SAVINGS = 'Savings'
    CURRENT = 'Current'
    OTHERS = 'Others'

    ACCOUNT_TYPE_CHOICES = [
        (SAVINGS, 'Savings'),
        (CURRENT, 'Current'),
        (OTHERS, 'Others'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    account_holder_name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=50)
    ifsc = models.CharField(max_length=20)
    account_type = models.CharField(max_length=50, choices=ACCOUNT_TYPE_CHOICES, default=SAVINGS)
    bank = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.account_holder_name}'s account ({self.account_number})"