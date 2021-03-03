from django.db import models
from django.contrib.auth.models import User
# Create your models here.

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

class UserDependents(models.Model):
    user = models.ForeignKey(User)

    dependents_age = models.PositiveIntegerField()
    dependents_name = models.CharField(max_length = 50)
    dependents_relation = models.CharField(max_length = 50)

    def __str__(self):
        return self.user.username

class userIncomeData(models.Model):
    user = models.ForeignKey(User)

    fixed_salary = models.PositiveIntegerField()
    variable_salary_min = models.PositiveIntegerField()
    variable_salary_max = models.PositiveIntegerField()

    def __str__(self):
        return self.user.username

class addUserExpense(models.Model):
    user = models.ForeignKey(User)

    expense_name =  models.CharField(max_length = 50,default = "")
    expense_date = models.DateField(default = "")
    expense_amount = models.PositiveIntegerField(default = 0)
    expense_repeat_frequency = models.PositiveIntegerField(default = 0)

class addUserInvestment(models.Model):
    user = models.ForeignKey(User)

    investment_name =  models.CharField(max_length = 50,default = "")
    investment_date = models.DateField(default = "")
    investment_amount = models.PositiveIntegerField(default = 0)
    investment_repeat_frequency = models.PositiveIntegerField(default = 0)
