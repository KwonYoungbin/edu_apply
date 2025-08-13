from django.db import models

class TestRegistration(models.Model):
    user_id = models.BigIntegerField()
    id = models.BigIntegerField()
    registered_at = models.DateTimeField()
    status = models.CharField(max_length=1)