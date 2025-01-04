from rest_framework import serializers
from .models import Client, Consumer, Account


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'name']


class ConsumerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consumer
        fields = ['id', 'name']


class AccountSerializer(serializers.ModelSerializer):
    client = ClientSerializer()
    consumers = ConsumerSerializer(many=True)

    class Meta:
        model = Account
        fields = ['id', 'client', 'consumers', 'balance', 'status']