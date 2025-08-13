from django.db import models

class CourseRegistration(models.Model):
    registered_at = models.DateTimeField()
    status = models.CharField(max_length=1)