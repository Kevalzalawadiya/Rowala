from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404, reverse

from utils.filehandler import handle_file_upload

from .forms import ProductForm, ComplainForm, InvoiceForm, InvoiceDetailForm, excelUploadForm, InvoiceDetailFormSet
from .models import Invoice, InvoiceDetail, Service, Product, Complain, BankAccount
import pandas as pd

from datetime import date, timedelta, datetime, timezone
import pdfkit

from dateutil.relativedelta import relativedelta

from django.db.models import Q
from django.db.models import Sum, Count

from django.http import JsonResponse
from django.utils import timezone

from django.db.models import Sum, Count
from django.db.models.functions import ExtractMonth

from datetime import *
from django.utils import timezone

from django.contrib.auth.decorators import login_required





# Create your views here.
@login_required(login_url='/accounts/login/')
def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


@login_required(login_url='/accounts/login/')
def base(request):
    total_invoice = Invoice.objects.filter(user=request.user).aggregate(
        sum=Sum('total'),
        all_invoices_count=Count('id')
    )
    context = {
        "total_invoice": total_invoice,
        "request": request
    }

    return render(request, "invoice/base/base.html", context)


@login_required(login_url='/accounts/login/')
def download_all(request):
    # Download all invoice to excel file
    # Download all product to excel file
    # Download all customer to excel file

    allInvoiceDetails = InvoiceDetail.objects.all()
    invoiceAndProduct = {
        "invoice_id": [],
        "invoice_date": [],
        "invoice_customer": [],
        "invoice_contact": [],
        "invoice_email": [],
        "invoice_comments": [],
        "product_name": [],
        "product_price": [],
        "product_unit": [],
        "product_amount": [],
        "invoice_total": [],

    }
    for curr in allInvoiceDetails:
        invoice = Invoice.objects.get(id=curr.invoice_id)
        product = Product.objects.get(id=curr.product_id)
        invoiceAndProduct["invoice_id"].append(invoice.id)
        invoiceAndProduct["invoice_date"].append(invoice.date)
        invoiceAndProduct["invoice_customer"].append(invoice.customer)
        invoiceAndProduct["invoice_contact"].append(invoice.contact)
        invoiceAndProduct["invoice_email"].append(invoice.email)
        invoiceAndProduct["invoice_comments"].append(invoice.comments)
        invoiceAndProduct["product_name"].append(product.product_name)
        invoiceAndProduct["product_price"].append(product.product_price)
        invoiceAndProduct["product_unit"].append(product.product_unit)
        invoiceAndProduct["product_amount"].append(curr.amount)
        invoiceAndProduct["invoice_total"].append(invoice.total)

    df = pd.DataFrame(invoiceAndProduct)
    df.to_excel("static/excel/allInvoices.xlsx", index=False)
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="allInvoices.xlsx"'
    with open("static/excel/allInvoices.xlsx", "rb") as f:
        response.write(f.read())
    return response


@login_required(login_url='/accounts/login/')
def delete_all_invoice(request):
    # Delete all invoice
    Invoice.objects.all().delete()
    return redirect("view_invoice")


@login_required(login_url='/accounts/login/')
def upload_product_from_excel(request):
    # Upload excel file to static folder "excel"
    # add all product to database
    # save product to database
    # redirect to view_product
    excelForm = excelUploadForm(request.POST or None, request.FILES or None)
    print("Reached HERE!")
    if request.method == "POST":
        print("Reached HERE2222!")

        handle_file_upload(request.FILES["excel_file"])
        excel_file = "static/excel/masterfile.xlsx"
        df = pd.read_excel(excel_file)
        Product.objects.all().delete()
        for index, row in df.iterrows():
            product = Product(
                product_name=row["product_name"],
                product_price=row["product_price"],
                product_unit=row["product_unit"],
            )
            print(product)
            product.save()
        return redirect("view_product")
    return render(request, "invoice/upload_products.html", {"excelForm": excelForm})


@login_required(login_url='/accounts/login/')
def create_product(request):
    total_invoice = Invoice.objects.filter(user=request.user).aggregate(
        sum=Sum('total'),
        all_invoices_count=Count('id')
    )

    product = ProductForm()

    if request.method == "POST":
        product = ProductForm(request.POST)
        if product.is_valid():
            product.save()
            return redirect("create_product")
    context = {
        "total_invoice": total_invoice,
        "product": product,
    }

    return render(request, "invoice/create_product.html", context)


@login_required(login_url='/accounts/login/')
def view_product(request):
    total_invoice = Invoice.objects.filter(user=request.user).aggregate(
        sum=Sum('total'),
        all_invoices_count=Count('id')
    )

    product = Product.objects.filter(product_is_delete=False)
    context = {
        "total_invoice": total_invoice,
        "product": product,
    }

    return render(request, "invoice/view_product.html", context)

@login_required(login_url='/accounts/login/')
def create_invoice(request):
    total_invoice = Invoice.objects.filter(user=request.user).aggregate(
        sum=Sum('total'),
        all_invoices_count=Count('id')
    )

    form = InvoiceForm()
    formset = InvoiceDetailFormSet()
    product_form = ProductForm()
    if request.method == "POST":
        form = InvoiceForm(request.POST)
        formset = InvoiceDetailFormSet(request.POST)
        product_form = ProductForm(request.POST)
        
        if form.is_valid():
            invoice = Invoice.objects.create(
                user = request.user,
                customer=form.cleaned_data.get("customer"),
                contact=form.cleaned_data.get("contact"),
                phone_number =form.cleaned_data.get("phone_number"),
                alt_phone_number =form.cleaned_data.get("alt_phone_number"),
                email=form.cleaned_data.get("email"),
                date=form.cleaned_data.get("date"), 
                subscription=form.cleaned_data.get("subscription"),
                is_bank_account=form.cleaned_data.get("is_bank_account"),                
            )
            print("-------------invoice date--------------->", invoice.date)


            # print("------------------>",invoice.subscription.months) #12
            # print("------------------>",invoice.subscription.service_period)
            enddate_date = invoice.date + relativedelta(months=invoice.subscription.months) #2024-11-7
            service_dates = invoice.date 
            service_number = 1
            while service_dates < enddate_date:
            # service date got at after 2 time
                print ("----->", service_dates) 
                service_dates = service_dates + relativedelta(months=invoice.subscription.service_period)
                Service.objects.create(
                    invoice = invoice,
                    service_date = service_dates,
                    complate_date = service_dates,
                    service_number = service_number
                )
                service_number +=1
            
        if formset.is_valid():
            total = 0
            for form in formset:
                product = Product.objects.create(
                    product_name = form.cleaned_data.get("product_name"),
                    product_price = form.cleaned_data.get("product_price"),
                    product_warranty = form.cleaned_data.get("product_warranty")
                )
                print(product)
                amount = form.cleaned_data.get("amount")
                if product and amount:
                    # Sum each row
                    sum = float(product.product_price) * float(amount)
                    # Sum of total invoice
                    total += sum
                    InvoiceDetail(
                        invoice=invoice, product=product, amount=amount
                    ).save()

            # Save the invoice
            invoice.total = total
            invoice.save()
            return redirect("view_invoice")
    context = {
        "total_invoice": total_invoice,
        "product_form": product_form,
        "form": form,
        "formset": formset,
    }

    return render(request, "invoice/create_invoice.html", context)

@login_required(login_url='/accounts/login/')
def all_service_management(request):
    total_invoice = Invoice.objects.filter(user=request.user).aggregate(
        sum=Sum('total'),
        all_invoices_count=Count('id')
    )
    today = timezone.now().date()
    tomorrow = today + timedelta(days=1)
    all_services = Service.objects.filter(service_date__range=[today, tomorrow]).order_by('service_date')
    service_count = Invoice.objects.filter(user=request.user)
    
    
    if request.method == "POST":        
        start_date_str = request.POST.get("start_date")
        end_date_str = request.POST.get("end_date") 
        
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

        all_services = Service.objects.filter(service_date__range=(start_date, end_date))

    context = {
        "total_invoice": total_invoice,
        "all_services": all_services,
        "service_count": service_count,
    }
    return render(request, "invoice/view_all_service.html", context)

@login_required(login_url='/accounts/login/')
def pending_service_management(request):
    total_invoice = Invoice.objects.filter(user=request.user).aggregate(
        sum=Sum('total'),
        all_invoices_count=Count('id')
    )
    today = timezone.now().date()
    all_services = Service.objects.filter(invoice__user=request.user, service_date=today, is_complate=False).order_by('service_date')
    service_count = Invoice.objects.filter(user=request.user)
    
    if request.method == "POST":        
        start_date_str = request.POST.get("start_date")
        end_date_str = request.POST.get("end_date") 
        
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

        all_services = Service.objects.filter(Q(invoice__user=request.user) &
                    Q(service_date__range=(start_date, end_date)) & Q(is_complate=False)
                ).order_by('service_date')   
        
    context = {
        "total_invoice": total_invoice,
        "all_services": all_services,
        "service_count": service_count,
    }
    return render(request, "invoice/view_pending_service.html", context)
    
    
@login_required(login_url='/accounts/login/')
def complate_service_management(request):
    total_invoice = Invoice.objects.filter(user=request.user).aggregate(
        sum=Sum('total'),
        all_invoices_count=Count('id')
    )
    today = timezone.now().date()
    all_services = Service.objects.filter(invoice__user=request.user, service_date=today, is_complate=True).order_by('service_date')
    service_count = Invoice.objects.filter(user=request.user)
    
    start_date_str = request.POST.get("start_date")
    end_date_str = request.POST.get("end_date") 

    if request.method == "POST":        
        start_date_str = request.POST.get("start_date")
        end_date_str = request.POST.get("end_date") 
        
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

        all_services = Service.objects.filter(Q(invoice__user=request.user) &
                    Q(service_date__range=(start_date, end_date)) & Q(is_complate=True)
                ).order_by('service_date')     
        
    context = {
        "total_invoice": total_invoice,
        "all_services":all_services,
        "service_count":service_count,
    }
    return render(request, "invoice/view_complate_service.html", context)

    
@login_required(login_url='/accounts/login/')
def service_status_change(request, pk):
    today = datetime.now().date()
    if request.method == "POST":
        one_service = Service.objects.get(id=pk)
        one_service.is_complate = True
        one_service.complate_date = today
        one_service.save()
        return redirect("dashboard")     
        
        
       
@login_required(login_url='/accounts/login/')
def view_invoice(request):
    total_invoice = Invoice.objects.filter(user=request.user).aggregate(
        sum=Sum('total'),
        all_invoices_count=Count('id')
    )

    invoice = Invoice.objects.filter(user=request.user).order_by('id')
    context = {
        "total_invoice": total_invoice,
        "invoice": invoice,
    }

    return render(request, "invoice/view_invoice.html", context)


# Detail view of invoices
@login_required(login_url='/accounts/login/')
def view_invoice_detail(request, pk):
    total_invoice = Invoice.objects.filter(user=request.user).aggregate(
        sum=Sum('total'),
        all_invoices_count=Count('id')
    )

    invoice = Invoice.objects.get(id=pk)
    invoice_detail = InvoiceDetail.objects.filter(invoice=invoice)
    context = {
        "total_invoice": total_invoice,
        'invoice': invoice,
        "invoice_detail": invoice_detail,
    }

    return render(request, "invoice/view_invoice_detail.html", context)

# @login_required(login_url='/accounts/login/')
def view_invoice_pdf_detail(request, id=None):
    invoice = get_object_or_404(Invoice, id=id)
    invoice_detail = InvoiceDetail.objects.filter(invoice=invoice)
    bank_details = BankAccount.objects.first()

    context = {
        "company": {
            "name": "Rowala",
            "phone_1": "+91 90164 67984 ",
            "phone_2": "+91 74349 16606 ",
            "web": "https://therowala.in/",
        },
        "invoice": invoice,
        "invoice_detail":invoice_detail,
        "invoice_id": "invoice.id",
        "invoice_total": "invoice.total_amount",
        "customer": "invoice.customer",
        "customer_email": "invoice.customer_email",
        "date": "invoice.date",
        "due_date": "invoice.due_date",
        "billing_address": "invoice.billing_address",
        "message": "invoice.message",
        "bank_details": bank_details,

    }
    return render(request, 'invoice/pdf_template.html', context)



# @login_required(login_url='/accounts/login/')
def generate_PDF(request, id):
    url = request.build_absolute_uri(reverse('view_invoice_pdf_detail', args=[id]))
    options = {
    'page-size': 'A4',
    'margin-top': '0.75in',
    'margin-right': '0.75in',
    'margin-bottom': '0.75in',
    'margin-left': '0.75in',
}
    pdf = pdfkit.from_url(url, False, options=options)
    response = HttpResponse(pdf,content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'

    return response



#  Delete invoice
@login_required(login_url='/accounts/login/')
def delete_invoice(request, pk):
    total_invoice = Invoice.objects.filter(user=request.user).aggregate(
        sum=Sum('total'),
        all_invoices_count=Count('id')
    )

    invoice = Invoice.objects.get(id=pk)
    invoice_detail = InvoiceDetail.objects.filter(invoice=invoice)
    if request.method == "POST":
        invoice_detail.delete()
        invoice.delete()
        return redirect("view_invoice")
    context = {
        "total_invoice": total_invoice,
        "invoice": invoice,
        "invoice_detail": invoice_detail,
    }

    return render(request, "invoice/delete_invoice.html", context)


# Edit product
@login_required(login_url='/accounts/login/')
def edit_product(request, pk):
    total_invoice = Invoice.objects.filter(user=request.user).aggregate(
        sum=Sum('total'),
        all_invoices_count=Count('id')
    )

    product = Product.objects.get(id=pk)
    form = ProductForm(instance=product)

    if request.method == "POST":
        product.save()
        return redirect("view_product")
    context = {
        "total_invoice": total_invoice,
        "product": form,
    }

    return render(request, "invoice/create_product.html", context)


# Delete product
@login_required(login_url='/accounts/login/')
def delete_product(request, pk):
    total_invoice = Invoice.objects.filter(user=request.user).aggregate(
        sum=Sum('total'),
        all_invoices_count=Count('id')
    )

    product = Product.objects.get(id=pk)

    if request.method == "POST":
        product.product_is_delete = True
        product.save()
        return redirect("view_product")
    context = {
        "total_invoice": total_invoice,
        "product": product,
    }

    return render(request, "invoice/delete_product.html", context)

# Complaints 
@login_required(login_url='/accounts/login/')
def list_complaints(request):
    total_invoice = Invoice.objects.filter(user=request.user).aggregate(
        sum=Sum('total'),
        all_invoices_count=Count('id')
    )
    total_complaints = Complain.objects.all()
    query = request.GET.get('query', '')
    find_user = Invoice.objects.filter(customer__icontains = query)
    forms = ComplainForm()
    if request.method == "POST":
        forms = ComplainForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('view-all-complaint')

    if is_ajax(request=request):
        # print(find_user.count())
        data_list = list(find_user.values())  # Convert queryset to list of dictionaries
        return JsonResponse(data_list, safe=False)

    
    context = {
        "total_invoice": total_invoice,
        "form": forms,
        "total_complaints":total_complaints,
    }
    return render(request, 'invoice/complains/view_all_complaints.html', context)


@login_required(login_url='/accounts/login/')
def dashboard(request):
    total_invoice = Invoice.objects.filter(user=request.user).aggregate(
        sum=Sum('total'),
        all_invoices_count=Count('id'),
    )
    monthly_totals = Invoice.objects.filter(user=request.user, date__year=date.today().year).annotate(
        month=ExtractMonth('date')
    ).values('month').annotate(
        total=Sum('total')
    ).order_by('month')
    today = timezone.now().date()
    tomorrow = today + timedelta(days=1)
    all_services = Service.objects.filter(invoice__user=request.user, service_date__range=[today, tomorrow]).order_by('service_date')
    service_count = Invoice.objects.filter(user=request.user)
    
    # last recent invoices 
    recent_invoice = Invoice.objects.filter(user=request.user).order_by('-date')[0:5]

    # Initialize lists for all 12 months with zero totals
    all_months = list(range(1, 13))
    totals = [0] * 12

    # Update totals for months with available data
    for month in monthly_totals:
        totals[month['month'] - 1] = month['total'] if 'total' in month else 0
    
    context = {
        "total_invoice": total_invoice,
        "months": all_months,
        "totals": totals,
        "recent_invoice": recent_invoice,
        "all_services": all_services,
        "service_count": service_count
    }
    return render(request, 'invoice/index.html', context)