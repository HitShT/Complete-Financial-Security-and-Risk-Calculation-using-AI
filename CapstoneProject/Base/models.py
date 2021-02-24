from django.db import models
from django.contrib.auth.models import User
# Create your models here.


# IDEA: Create 2 different tables, better, easier readability
class presentAssetsData(models.Model):
    user = models.ForeignKey(User)

    assets_name = models.CharField(max_length = 50,blank=True,default="")
    assets_valuation = models.FloatField(blank=True,default=0)
    
    def __str__(self):
        return self.user.username

class presentLiabilitiesData(models.Model):
    user = models.ForeignKey(User)

    liabilities_name = models.CharField(max_length = 50,default="",blank=True)
    liabilities_valuation = models.FloatField(default=0,blank=True)

    def __str__(self):
        return self.user.username
