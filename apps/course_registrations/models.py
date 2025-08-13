from django.db import models
from apps.users.models import User

class CourseRegistration(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    item_id = models.BigIntegerField()
    registered_at = models.DateTimeField()