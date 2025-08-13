from django.db import models
from apps.users.models import User

class TestRegistration(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    item_id = models.BigIntegerField()
    registered_at = models.DateTimeField(auto_now_add=True)