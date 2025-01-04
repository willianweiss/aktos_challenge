from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Client, Account, Consumer
from .serializers import AccountSerializer
import csv


class AccountListView(ListAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['balance', 'status', 'consumers__name']

    def get_queryset(self):
        min_balance = self.request.query_params.get('min_balance')
        max_balance = self.request.query_params.get('max_balance')
        queryset = super().get_queryset()

        if min_balance:
            queryset = queryset.filter(balance__gte=min_balance)
        if max_balance:
            queryset = queryset.filter(balance__lte=max_balance)

        return queryset


class CSVUploadView(APIView):
    def post(self, request, *args, **kwargs):
        if 'file' not in request.FILES:
            return Response({"error": "File not provided. Please upload a CSV file."}, status=400)

        file = request.FILES['file']
        decoded_file = file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)

        required_fields = ['client reference no', 'balance', 'status', 'consumer name']
        missing_fields = [field for field in required_fields if field not in reader.fieldnames]
        if missing_fields:
            return Response({
                "error": "Missing required fields in CSV",
                "missing_fields": missing_fields
            }, status=400)

        for row in reader:
            client, _ = Client.objects.get_or_create(name=row['client reference no'])

            consumer, _ = Consumer.objects.get_or_create(name=row['consumer name'])

            account, _ = Account.objects.get_or_create(
                client=client,
                balance=row['balance'],
                status=row['status']
            )

            account.consumers.add(consumer)

        return Response({"message": "CSV file processed successfully"})