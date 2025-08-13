from django.db import models

class Test(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=200)
    started_at = models.DateTimeField(null=False)
    ended_at = models.DateTimeField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)