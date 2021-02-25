from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
# Create your views here.

def getData(response):
    if response.method == "POST":
        print(response.POST)
    return render(response,"HealthInsurancePredict\getData.html")
