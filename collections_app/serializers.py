from rest_framework import serializers
from .models import Account, Client, Consumer


class ConsumerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consumer
        fields = ["id", "name"]


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ["id", "name"]


class AccountSerializer(serializers.ModelSerializer):
    client = ClientSerializer()
    consumers = ConsumerSerializer(many=True)

    class Meta:
        model = Account
        fields = ["id", "client", "consumers", "balance", "status"]
