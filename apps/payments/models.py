from django.db import models

class Payment(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.BigIntegerField()
    item_type = models.CharField(max_length=1)
    item_id = models.BigIntegerField()
    amount = models.IntegerField()
    method = models.CharField(max_length=20)
    status = models.CharField(max_length=1)
    paid_at = models.DateTimeField(auto_now_add=True)
    canceled_at = models.DateTimeField()`