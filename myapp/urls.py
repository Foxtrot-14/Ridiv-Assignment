# urls.py

from django.urls import path
from .views import InvoiceList, InvoiceDetailView

urlpatterns = [
    path('invoices/', InvoiceList.as_view(), name='invoices'),
    path('invoices/<int:pk>/', InvoiceDetailView.as_view(), name='invoice-detail'),
]
