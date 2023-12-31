from rest_framework import serializers
from .models import Invoice, InvoiceDetail

class InvoiceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceDetail
        fields = ['id', 'invoice', 'description', 'quantity', 'unit_price', 'price']
        
class InvoiceSerializer(serializers.ModelSerializer):
    invoice_details = InvoiceDetailSerializer(many=True, required=False)

    class Meta:
        model = Invoice
        fields = ['id', 'date', 'customer_name', 'invoice_details']        
    