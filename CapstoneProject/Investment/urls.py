from django.conf.urls import url,include
from django.contrib import admin
from . import views
urlpatterns = [
    url(r"^getEquity/",views.showEquity),
    url(r"^getMF/",views.showMF),
    url(r"^decideType",views.showTypePrediction)
]
