from django import forms
from django.forms import formset_factory
from django.contrib.auth.models import AbstractBaseUser

from .models import Product, Invoice, InvoiceDetail, Complain


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "product_name",
            "product_price",
            "product_unit",
        ]
        widgets = {
            "product_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "id": "product_name",
                    "placeholder": "Enter name of product",
                }
            ),
            "product_price": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "id": "product_price",
                    "placeholder": "Enter price of product",
                    "type": "number",
                    "required": "required",
                }
            ),
            "product_unit": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "id": "product_unit",
                    "placeholder": "Enter unit of product",
                }
            ),
        }

class ComplainForm(forms.ModelForm):
    class Meta:
        model = Complain
        fields = ['invoice', 'description']
        widgets = {
            "invoice": forms.Select(
                attrs={
                    "class": "js-example-placeholder-single js-states form-control",
                    "id": "invoice_detail_product",
                    "required": "required",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class":"form-control",
                    "required":"required"
                }
            ),
        }

class InvoiceForm(forms.ModelForm):
    is_bank_account = forms.BooleanField(required=False)
    class Meta:
        model = Invoice
        fields = [
            "date",
            "customer",
            "phone_number",
            "alt_phone_number",
            "contact",
            "email",
            "subscription",
            "is_bank_account"
            
        ]
        widgets = {
            "date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "id":"start_date",
                    "required": "required",
                    "type": "date"
                }
            ),
            "customer": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "id": "invoice_customer",
                    "placeholder": "Customer Name",
                }
            ),
            "contact": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "id": "invoice_contact",
                    "placeholder": "Street Address City State",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "id": "invoice_email",
                    "placeholder": "customer@gmail.com",
                }
            ),
            "phone_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "id": "invoice_comments",
                    "placeholder": "Enter Mobile number of customer",
                }
            ),
            "alt_phone_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "id": "invoice_comments",
                    "placeholder": "Alternative phone number of customer",
                }
            ),
            "subscription": forms.Select(
                attrs={
                    "class": "form-control",
                    "id": "invoice_detail_product",
                    "required": "required",
                }
            )
        }

    def __init__(self, *args, **kwargs):
        super(InvoiceForm, self).__init__(*args, **kwargs)
        self.fields["subscription"].empty_label = None


class InvoiceDetailForm(forms.ModelForm):
    product_warranty = forms.ChoiceField(
        choices=Product.WARRANTY_CHOICES,
        widget=forms.Select(
            attrs={
                "class": "form-control selectpicker",
                "id": "product_warranty",
                "required": "required",
            }
        ),
    )

    class Meta:
        model = InvoiceDetail
        fields = [
            "amount",
        ]
        widgets = {
            "amount": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "id": "invoice_detail_amount",
                    "placeholder": "0",
                    "type": "number",
                    "required": "required",
                }
            ),
        }

    product_name = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "product_name",
                "placeholder": "Enter name of the product",
                "required": "required",
            }
        ),
    )
    product_price = forms.FloatField(
        required=False,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "id": "product_price",
                "placeholder": "Enter price of the product",
                "type": "number",
                "required": "required",
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        super(InvoiceDetailForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.product:
            product = self.instance.product
            self.fields["product_name"].initial = product.product_name
            self.fields["product_price"].initial = product.product_price


class excelUploadForm(forms.Form):
    file = forms.FileField()


InvoiceDetailFormSet = formset_factory(InvoiceDetailForm, extra=1)


# class EmpDetailsForm(forms.Form): 
#     agree = forms.BooleanField( 
#         label='Agree', 
#         required = True, 
#         disabled = False, 
#         widget=forms.widgets.CheckboxInput( 
#             attrs={'class': 'checkbox-inline'}), 
#             help_text = "I accept the terms in the License Agreement",
#             error_messages ={'required':'Please check the box'}
#             )