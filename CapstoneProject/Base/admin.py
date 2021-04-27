from django.contrib import admin
from .models import presentAssetsData,presentLiabilitiesData,UserDependents,userIncomeData,addUserExpense,addUserInvestment,allPredictionsData
# Register your models here.

admin.site.register(presentAssetsData)
admin.site.register(presentLiabilitiesData)
admin.site.register(UserDependents)
admin.site.register(userIncomeData)
admin.site.register(addUserExpense)
admin.site.register(addUserInvestment)
admin.site.register(allPredictionsData)
