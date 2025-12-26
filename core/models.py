from django.db import models
from accounts.models import User
from django_jalali.db import models as jmodels
from django.utils import timezone

# Create your models here.
class Task(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='tasks')
    title = models.CharField(max_length=255)
    reminder_date = models.DateField(blank=True,null=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.title