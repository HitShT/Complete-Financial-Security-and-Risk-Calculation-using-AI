from django.contrib import admin
from .models import investmentAreas,investmentDivision,investmentRiskLiquidity
# Register your models here.

admin.site.register(investmentAreas)
admin.site.register(investmentDivision)
admin.site.register(investmentRiskLiquidity)
