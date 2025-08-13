from django.db import models
from apps.users.models import User

class Payment(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    item_type = models.CharField(max_length=1)  # 'T': Test, 'C': Course
    item_id = models.BigIntegerField()
    amount = models.IntegerField()
    method = models.CharField(max_length=20)
    status = models.CharField(max_length=1)     # 'P': Paid, 'C': Canceled
    paid_at = models.DateTimeField(auto_now_add=True)
    canceled_at = models.DateTimeField(null=True)