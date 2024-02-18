from django.urls import path
from . import views


urlpatterns = [
    path('home', views.create_invoice, name='home'),
    path('', views.dashboard, name='dashboard'),
    path('create_product/', views.create_product, name='create_product'),
    path('view_product/', views.view_product, name='view_product'),
    path('edit_product/<int:pk>', views.edit_product, name='edit_product'),
    path('delete_product/<int:pk>/', views.delete_product, name='delete_product'),
    path('upload_product_excel', views.upload_product_from_excel, name='upload_product_excel'),
    # path('create_customer/', views.create_customer, name='create_customer'),
    # path('view_customer/', views.view_customer, name='view_customer'),
    # path('edit_customer/<int:pk>', views.edit_customer, name='edit_customer'),
    # path('delete_customer/<int:pk>/', views.delete_customer, name='delete_customer'),

    path('create_invoice/', views.create_invoice, name='create_invoice'),
    path('view_invoice/', views.view_invoice, name='view_invoice'),
    path('delete_invoice/<int:pk>/', views.delete_invoice, name='delete_invoice'),
    path('delete_all_invoice/', views.delete_all_invoice, name='delete_all_invoice'),
    path('download_all_invoice/', views.download_all, name='download_all_invoice'),
    path('view_invoice_detail/<int:pk>/', views.view_invoice_detail, name='view_invoice_detail'),
    path('invoice-detail/<id>/', views.view_invoice_pdf_detail, name='view_invoice_pdf_detail'),
    path('invoice-download/<id>/', views.generate_PDF, name='invoice-download'),
    path('view_all_service/', views.all_service_management, name='service-view-all'),
    path('view_pending_service/', views.pending_service_management, name='service-view-pending'),
    path('view_complate_service/', views.complate_service_management, name='service-view-complate'),
    path('service_status_change/<int:pk>', views.service_status_change, name="service_status_change"),

    # Complaint urls
    path('view_all_complaint/', views.list_complaints, name='view-all-complaint')    
     
]
