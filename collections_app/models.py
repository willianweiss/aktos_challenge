from django.db import models


class Client(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Consumer(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Account(models.Model):
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="accounts"
    )
    consumers = models.ManyToManyField(Consumer, related_name="accounts")
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"Account: {self.id} - {self.client.name}"
