from django.db import models
from apps.users.models import User
from apps.tests.models import Test

class TestRegistration(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    test = models.ForeignKey(
        Test,
        on_delete=models.CASCADE
    )
    registered_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)