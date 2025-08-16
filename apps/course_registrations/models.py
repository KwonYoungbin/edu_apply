from django.db import models
from apps.users.models import User
from apps.courses.models import Course

class CourseRegistration(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE
    )
    registered_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)