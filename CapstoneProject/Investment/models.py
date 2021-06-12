from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class investmentAreas(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    investmentName = models.CharField(max_length = 100)
    investmentQuantity = models.FloatField()
    investmentAmount =  models.FloatField()

class investmentDivision(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    investmentType = models.CharField(max_length = 100,default="NA")
    investmentPercentage = models.FloatField(default = 0)

class investmentRiskLiquidity(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    risk = models.IntegerField()
    liquidity = models.IntegerField()
