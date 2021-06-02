from django.shortcuts import render
from django.http import HttpResponse
from Base import gradeAndPredict
from Base.models import allPredictionsData,UserDependents,presentAssetsData
from django.contrib.auth.models import User

# Create your views here.
def showEquity(response):
    stock = [
        ["ABC",1,40],
        ["DEF",3,20],
        ["GHI",12,34]
    ]

    qty = 0
    price = 0

    for i in range(len(stock)):
        stock[i] = [i+1]+stock[i]
        stock[i].append(stock[i][-2]*stock[i][-1])
        qty += stock[i][2]
        price += stock[i][-1]

    context = {
        "amount_invest" : 456,
        "stocks" : stock,
        "qtyStocks" : qty,
        "priceStocks" : price
    }
    return render(response,"Investment/showEquity.html",context)

def showMF(response):
    MF = [
        ["ABC",1,40],
        ["DEF",3,20],
        ["GHI",12,34]
    ]

    qty = 0
    price = 0

    for i in range(len(MF)):
        MF[i] = [i+1]+MF[i]
        MF[i].append(MF[i][-2]*MF[i][-1])
        qty += MF[i][2]
        price += MF[i][-1]

    context = {
        "amount_invest" : 456,
        "MF" : MF,
        "qtyMF" : qty,
        "priceMF" : price
    }
    return render(response,"Investment/showMF.html",context)

def showTypePrediction(response):
    monthly_salary,monthly_expense,expenses_yearly,age,dependents,presentInvestmentValue,presentInvestmentMonthly,presentInvestmentRate,presentHealthInsuranceValue,futureDependents,highLiquid,healthInsurancePremium = 0,0,0,0,0,0,0,0,0,0,0,0

    ob = allPredictionsData.objects.filter(user=User.objects.get(username=response.user.username))

    for i in ob:
        monthly_salary = i.monthly_salary
        monthly_expense = i.monthly_expense
        expense_yearly = i.yearly_expense
        age = i.age
        dependents = i.dependents
        presentInvestmentMonthly = i.investmentMonthly
        presentInvestmentRate = 8.5
        presentHealthInsuranceValue = i.healthInsurance
        presentInvestmentValue = i.investmentTotal
        highLiquid = i.highLiquid
        healthInsurancePremium = i.healthInsurancePremium
        highLiquid = i.highLiquid
        healthInsurancePremium = i.healthInsurancePremium

    ob = gradeAndPredict.gradeExisting(monthly_salary,monthly_expense,expenses_yearly,age,dependents,presentInvestmentValue,presentInvestmentMonthly,presentInvestmentRate,presentHealthInsuranceValue,futureDependents,highLiquid,healthInsurancePremium)

    return HttpResponse(str(ob.retirementSave))
