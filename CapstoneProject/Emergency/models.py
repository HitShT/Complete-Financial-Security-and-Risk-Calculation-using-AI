from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class emergencyInvestment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    investmentName =  models.CharField(max_length = 100)
    investmentQuantity = models.IntegerField()
    investmentPrice = models.FloatField()
