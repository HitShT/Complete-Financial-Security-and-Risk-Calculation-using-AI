from django.conf.urls import url,include
from django.contrib import admin
from Base import views

app_name = "Base"

urlpatterns = [
    url(r"^register/$",views.userRegister,name="register"),
    url(r"^login/$",views.userLogin,name="login"),
    url(r"^logout/$",views.userLogout,name = "logout"),
    url(r"^check/$",views.check),
    url(r"^getUserAssets/$",views.getUserAssets,name = 'getAssets'),
    url(r"^getUserLiabilities/$",views.getUserLiabilities,name = 'getLiabilities'),
    url(r'^getUserDependents/$',views.getUserDependents,name = 'getDependents'),
    url(r'^getUserIncome/$',views.getUserIncomeData,name = 'getMonthlyIncome'),
    url(r"^getRepeatingExpenseData/$",views.getUserExpenseData,name = "getRepeatingExpense"),
    url(r"^getRepeatingInvestmentData/$",views.getUserInvestmentData,name = "getRepeatingInvestment"),
    url(r"^getUserPredictionValues/$",views.getUserPredictionValues,name = "getUserPredictionData"),
    url(r"^showDisplayBoxes/$",views.showBuckets),
    url(r"^financialSecurityOverview/$",views.financialOverview)
    ]

# getUserPredictionValues
