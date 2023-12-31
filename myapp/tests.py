from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Invoice, InvoiceDetail

class InvoiceAPITestCase(APITestCase):
    def setUp(self):
        self.invoice_data = {
            "date": "2023-12-31",
            "customer_name": "John Doe Test",
            "invoice_details": [
                {
                    "description": "Product 1",
                    "quantity": 2,
                    "unit_price": "25",
                    "price": "50"
                },
                {
                    "description": "Product 2",
                    "quantity": 1,
                    "unit_price": "30",
                    "price": "30"
                }
            ]
        }

    def test_create_invoice_with_details(self):
        url = '/invoices/1/'
        response = self.client.post(url, self.invoice_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        invoice_count = Invoice.objects.count()
        invoice_detail_count = InvoiceDetail.objects.count()
        self.assertEqual(invoice_count, 1)
        self.assertEqual(invoice_detail_count, 2)

    def test_retrieve_invoice_list(self):
        url = reverse('invoices')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_update_invoice_with_details(self):
        # Create an invoice first
        create_url = '/invoices/1/'  # Endpoint for creating invoices
        create_response = self.client.post(create_url, self.invoice_data, format='json')
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        invoice_id = 1

        # Update the created invoice
        update_url = f'/invoices/{invoice_id}/'  # Endpoint for updating a specific invoice
        updated_invoice_data = {
            "date": "2023-12-31",
            "customer_name": "Updated Customer",
            "invoice_details": [
                {
                    "description": "Updated Product 1",
                    "quantity": 3,
                    "unit_price": "30",
                    "price": "90"
                },
                {
                    "description": "Updated Product 2",
                    "quantity": 2,
                    "unit_price": "40",
                    "price": "80"
                }
            ]
        }
        response = self.client.put(update_url, updated_invoice_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify the updated data
        updated_invoice = Invoice.objects.get(pk=invoice_id)
        self.assertEqual(updated_invoice.customer_name, "Updated Customer")
        # Add further assertions for the updated details

    def test_delete_invoice(self):
        # Create an invoice first
        create_url = '/invoices/1/'  # Endpoint for creating invoices
        create_response = self.client.post(create_url, self.invoice_data, format='json')
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        invoice_id = 1

        # Delete the created invoice
        delete_url = f'/invoices/{invoice_id}/'  # Endpoint for deleting a specific invoice
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify that the invoice is deleted
        with self.assertRaises(Invoice.DoesNotExist):
            Invoice.objects.get(pk=invoice_id)