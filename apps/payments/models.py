from django.db import models
from apps.users.models import User

class Payment(models.Model):
    ITEM_TYPE_CHOICES = [
        ('T', '시험'),
        ('C', '수업'),
    ]

    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    item_type = models.CharField(max_length=1, choices=ITEM_TYPE_CHOICES)  # 'T': Test, 'C': Course
    item_id = models.BigIntegerField()
    item_title = models.CharField(max_length=200, null=True)
    amount = models.IntegerField()
    method = models.CharField(max_length=20)
    status = models.CharField(max_length=1, default='P')     # 'P': Paid, 'C': Canceled
    paid_at = models.DateTimeField(auto_now_add=True)
    canceled_at = models.DateTimeField(null=True)

    original_price = models.IntegerField(null=True)
    discounted_price = models.IntegerField(null=True)