# views.py
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import *
from .renderers import *
from .models import Invoice, InvoiceDetail

class InvoiceList(APIView):
    renderer_classes = [UserRenderer]
    def get(self,request,*args,**kwargs):
        data = Invoice.objects.all()
        serializer = InvoiceSerializer(data,many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)

class InvoiceDetailView(APIView):
    renderer_classes = [UserRenderer]
    def get_object(self, pk):
        try:
            return InvoiceDetail.objects.get(pk = pk)
        except InvoiceDetail.DoesNotExist:
            return None
        
    def get(self,request,pk,*args,**kwargs):
        post = self.get_object(pk)
        if post is None:
            return Response({'error': 'Invoice not found'}, status = status.HTTP_404_NOT_FOUND)
        else:
            serializer = InvoiceDetailSerializer(post)
            return Response(serializer.data, status = status.HTTP_200_OK)
        
    def post(self, request, *args, **kwargs):
        invoice_data = request.data
        invoice_details_data = invoice_data.pop('invoice_details', [])

        invoice_serializer = InvoiceSerializer(data=invoice_data)
        if invoice_serializer.is_valid():
            invoice = invoice_serializer.save()
            for detail_data in invoice_details_data:
                detail_data['invoice'] = invoice.id  # Set the invoice foreign key
                detail_serializer = InvoiceDetailSerializer(data=detail_data)
                if detail_serializer.is_valid():
                    detail_serializer.save()
                else:
                    # Handle invalid detail data here
                    return Response(detail_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response({'msg': 'Invoice added'}, status=status.HTTP_201_CREATED)
        return Response(invoice_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk, *args, **kwargs):
        invoice = Invoice.objects.get(pk=pk)
        invoice_data = request.data
        invoice_details_data = invoice_data.pop('invoice_details', [])

        invoice_serializer = InvoiceSerializer(instance=invoice, data=invoice_data)
        if invoice_serializer.is_valid():
            updated_invoice = invoice_serializer.save()

            # Update or Create InvoiceDetails manually
            for detail_data in invoice_details_data:
                detail_data['invoice'] = updated_invoice.id  # Set the invoice foreign key
                if 'id' in detail_data:
                    detail_instance = InvoiceDetail.objects.get(pk=detail_data['id'])
                    detail_serializer = InvoiceDetailSerializer(instance=detail_instance, data=detail_data)
                else:
                    detail_serializer = InvoiceDetailSerializer(data=detail_data)

                if detail_serializer.is_valid():
                    detail_serializer.save()
                else:
                    # Handle invalid detail data here
                    return Response(detail_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response({'msg': 'Invoice updated'}, status=status.HTTP_200_OK)
        return Response(invoice_serializer.errors, status=status.HTTP_400_BAD_REQUEST)      
    
    def delete(self, request, pk, *args, **kwargs):
        try:
            invoice = Invoice.objects.get(pk=pk)
        except Invoice.DoesNotExist:
            return Response({'msg': 'Invoice does not exist'}, status=status.HTTP_404_NOT_FOUND)

        invoice.delete()
        return Response({'msg': 'Invoice deleted'}, status=status.HTTP_204_NO_CONTENT)