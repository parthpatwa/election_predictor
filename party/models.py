from django.db import models
from authentication.models import Party
import uuid
from random import seed


def random_transaction_id():
    seed()
    transaction_id = "ADD" + uuid.uuid4().hex[:9].upper()
    return transaction_id


class PaymentDetails(models.Model):
    party = models.ForeignKey(Party, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=14, default=random_transaction_id(), null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    credits = models.FloatField(null=True)
