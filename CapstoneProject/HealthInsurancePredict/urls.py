from django.conf.urls import url,include
from django.contrib import admin
from HealthInsurancePredict import views

app_name = "HealthInsurancePredict"

urlpatterns = [
    url(r"^choice/$",views.getData),
    url(r"predictionData/$",views.predictionData)
    ]
