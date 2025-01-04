from rest_framework.test import APITestCase
from rest_framework import status
from .models import Client, Consumer, Account

class AccountFilterTests(APITestCase):
    def setUp(self):
        client = Client.objects.create(name="Client A")
        consumer = Consumer.objects.create(name="John Doe")
        account = Account.objects.create(client=client, balance=500.00, status="in_collection")
        account.consumers.add(consumer)

    def test_filter_by_min_balance(self):
        response = self.client.get('/api/accounts/?min_balance=100')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_filter_by_status(self):
        response = self.client.get('/api/accounts/?status=in_collection')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_filter_by_consumer_name(self):
        response = self.client.get('/api/accounts/?consumer_name=John Doe')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)