from django.db import models

class Course(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=200)
    start_at = models.DateTimeField(null=False)
    end_at = models.DateTimeField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
