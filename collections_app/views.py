from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.pagination import LimitOffsetPagination
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Client, Account, Consumer
from .serializers import AccountSerializer
import csv


class AccountListView(ListAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    filter_backends = [DjangoFilterBackend]
    pagination_class = LimitOffsetPagination

    @swagger_auto_schema(
        operation_description="Retrieve a list of accounts with optional filters",
        manual_parameters=[
            openapi.Parameter(
                name="min_balance",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_NUMBER,
                description="Minimum balance to filter accounts",
            ),
            openapi.Parameter(
                name="max_balance",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_NUMBER,
                description="Maximum balance to filter accounts",
            ),
            openapi.Parameter(
                name="status",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Filter accounts by status (e.g., 'INACTIVE', 'PAID_IN_FULL')",
            ),
            openapi.Parameter(
                name="consumer_name",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Filter accounts by consumer name (case-insensitive match)",
            ),
        ],
        responses={
            200: openapi.Response(
                description="List of accounts",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "count": openapi.Schema(
                            type=openapi.TYPE_INTEGER,
                            description="Total number of accounts",
                        ),
                        "next": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="URL for the next page",
                        ),
                        "previous": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="URL for the previous page",
                        ),
                        "results": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_OBJECT),
                        ),
                    },
                ),
            )
        },
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        min_balance = self.request.query_params.get("min_balance")
        max_balance = self.request.query_params.get("max_balance")
        status = self.request.query_params.get("status")
        consumer_name = self.request.query_params.get("consumer_name")

        queryset = super().get_queryset()

        if min_balance:
            queryset = queryset.filter(balance__gte=min_balance)

        if max_balance:
            queryset = queryset.filter(balance__lte=max_balance)

        if status:
            queryset = queryset.filter(status=status)

        if consumer_name:
            queryset = queryset.filter(consumers__name__icontains=consumer_name)

        return queryset


class CSVUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        operation_description="Upload a CSV file to process consumer account data.",
        manual_parameters=[
            openapi.Parameter(
                name="file",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_FILE,
                description="The CSV file to upload",
                required=True,
            )
        ],
        responses={
            200: openapi.Response(
                description="CSV file processed successfully",
                examples={
                    "application/json": {"message": "CSV file processed successfully"}
                },
            ),
            400: openapi.Response(
                description="Error in file upload",
                examples={
                    "application/json": {
                        "error": "File not provided. Please upload a CSV file.",
                        "missing_fields": ["field1", "field2"],
                    }
                },
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        if "file" not in request.FILES:
            return Response(
                {"error": "File not provided. Please upload a CSV file."}, status=400
            )

        file = request.FILES["file"]
        decoded_file = file.read().decode("utf-8").splitlines()
        reader = csv.DictReader(decoded_file)

        required_fields = ["client reference no", "balance", "status", "consumer name"]
        missing_fields = [
            field for field in required_fields if field not in reader.fieldnames
        ]
        if missing_fields:
            return Response(
                {
                    "error": "Missing required fields in CSV",
                    "missing_fields": missing_fields,
                },
                status=400,
            )

        for row in reader:
            client, _ = Client.objects.get_or_create(name=row["client reference no"])

            consumer, _ = Consumer.objects.get_or_create(name=row["consumer name"])

            account, _ = Account.objects.get_or_create(
                client=client, balance=row["balance"], status=row["status"]
            )

            account.consumers.add(consumer)

        return Response({"message": "CSV file processed successfully"})
