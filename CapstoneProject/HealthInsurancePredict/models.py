from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class healthInsuranceSelected(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    plan = models.CharField(max_length = 100)
    company = models.CharField(max_length = 100)
    amount = models.IntegerField()
    premium = models.IntegerField()
