from django.db import models
from django.utils import timezone


# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=255)
    product_price = models.FloatField(default=0)
    product_unit = models.CharField(max_length=255, null=True, blank=True)
    product_is_delete = models.BooleanField(default=False)

    def __str__(self):
        return str(self.product_name)


# class Customer(models.Model):
#     GENDER_CHOICES = (
#         ('Male', 'Male'),
#         ('Female', 'Female'),
#         ('Others', 'Others'),
#     )
#     customer_name = models.CharField(max_length=255)
#     customer_gender = models.CharField(max_length=50, choices=GENDER_CHOICES)
#     customer_dob = models.DateField()
#     customer_points = models.IntegerField(default=0)

#     def __str__(self):
#         return str(self.customer_name)


class Subscription(models.Model):
    months = models.IntegerField()
    # months = models.PositiveIntegerField(default=0)
    service_period = models.IntegerField(help_text='Enter number of mounth in which you want to give services.')

    def __str__(self):
        return f"{self.service_period} Services for {self.months}-months "


class Invoice(models.Model):
    date = models.DateField(auto_now_add=True)
    customer = models.TextField(default='')
    contact = models.CharField(
        max_length=255, default='', blank=True, null=True) # Address field
    email = models.EmailField(default='', blank=True, null=True)
    comments = models.BigIntegerField(blank=True, null=True) # Mobile Number field
    total = models.FloatField(default=0)
    subscription = models.ForeignKey(
        Subscription, on_delete=models.SET_NULL, blank=True, null=True
)


    def __str__(self):
        return str(self.id)
    
    @property
    def get_total_bill(self):
        invoices = self.invoice.all()
        total = 0
        for invoice in invoices:
            total += float(invoice.product.product_price) * float(invoice.amount)
        return total





class InvoiceDetail(models.Model):
    invoice = models.ForeignKey(
        Invoice, on_delete=models.SET_NULL, blank=True, null=True, related_name='invoice')
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.IntegerField(default=1)

    @property
    def get_total_bill(self):
        total = float(self.product.product_price) * float(self.amount)
        return total




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