import uuid
from django.db import models


class DelivererModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=30)
    region = models.CharField(max_length=80)
    status = models.CharField(max_length=20)

    class Meta:
        db_table = 'deliverers'


class OrderModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    region = models.CharField(max_length=80)
    status = models.CharField(max_length=20)
    assigned_deliverer_id = models.UUIDField(null=True, blank=True)

    class Meta:
        db_table = 'orders'
