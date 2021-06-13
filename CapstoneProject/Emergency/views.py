from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
# Create your views here.
from Base import gradeAndPredict
from Investment import planExpense
import datetime
from Base.models import allPredictionsData
from Base.models import addUserExpense,addUserInvestment,allPredictionsData,UserDependents,presentAssetsData
from django.contrib.auth.models import User
from .models import emergencyInvestment

variablesPortfolio = {}

def addMonths(start,duration):
    date,month,year = start.day,start.month+duration,start.year
    addYears = month//12
    month = month%12 + 1
    year += addYears
    return datetime.date(year,month,date)

def test(response):
    # emergencyInvestment.emergencyInvestment(4500)
    liabilities = addUserExpense.objects.filter(user=User.objects.get(username=response.user.username))
    assets = addUserInvestment.objects.filter(user=User.objects.get(username=response.user.username))
    ct = 1
    expenses = []
    today = datetime.date.today()
    totalPortfolio = {}
    for i in assets:
        temp = [ct,"Asset",i.investment_name,i.investment_date,i.investment_duration_count,i.investment_amount]
        ans = i.investment_date
        finalDate = addMonths(ans,i.investment_duration_count)
        ct += 1
        temp.append(today>finalDate)
        if temp[-1]:
            temp.append(0)
        else:
            ob = planExpense.planExpense(i.investment_amount,12/i.investment_repeat_frequency)
            temp.append(sum([ob.portfolio[i] for i in ob.portfolio]))
            for i in ob.portfolio:
                if i not in totalPortfolio:
                    totalPortfolio[i] = ob.portfolio[i]
                else:
                    totalPortfolio[i] += ob.portfolio[i]
            temp[-1] = round(temp[-1],2)
        expenses.append(temp)

    for i in liabilities:
        temp = [ct,"Liabilities",i.expense_name,i.expense_date,i.expense_duration_count,i.expense_amount]
        ans = i.expense_date
        finalDate = addMonths(ans,i.expense_duration_count)
        ct += 1
        temp.append(today>finalDate)
        if temp[-1]:
            temp.append(0)
        else:
            ob = planExpense.planExpense(i.expense_amount,12/i.expense_repeat_frequency)
            temp.append(sum([ob.portfolio[i] for i in ob.portfolio]))
            for i in ob.portfolio:
                if i not in totalPortfolio:
                    totalPortfolio[i] = ob.portfolio[i]
                else:
                    totalPortfolio[i] += ob.portfolio[i]
            temp[-1] = round(temp[-1],2)
        expenses.append(temp)

    ctxt = {'expense' : expenses}

    if response.method == 'POST':
        if "portfolio1" in response.POST:
            print("test")

    return render(response,"Emergency/baseEmergency.html",context = ctxt)

def saveAmount(response):
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

    job_loss = ob.job_loss
    job_loss = [round(i,2) for i in job_loss]

    if response.method == "POST":
        if response.POST.get("press"):
            form_response = response.POST
            ob = planExpense.planExpense(float(form_response["amount"]),12)
            portfolio = ob.portfolio
            ct = 1
            tt = 0
            for i in portfolio:
                portfolio[i] = [round(portfolio[i][j],2) for j in range(2)]
                if(i == "Savings"):
                    portfolio[i].append(portfolio[i][0])
                else:
                    portfolio[i].append(round(portfolio[i][0]*portfolio[i][1],2))
                tt += portfolio[i][-1]
                portfolio[i] = [ct]+portfolio[i]
                ct += 1
            tt = round(tt,2)
            tempp = []
            for i in portfolio:
                tp = [portfolio[i][0],i,portfolio[i][1],portfolio[i][2],portfolio[i][3]]
                tempp.append(tp)
            portfolio = tempp.copy()

            userObject = User.objects.get(username=response.user.username)

            emergencyInvestment.objects.filter(user = userObject).delete()

            for i in portfolio:
                emergencyInvestment(user = userObject,investmentName = i[1],investmentQuantity = i[2],investmentPrice = i[3]).save()

            return render(response,"Emergency/emergencyPredict.html",{"minSave":min(job_loss),"maxSave":max(job_loss),"portfolio":portfolio,"total":tt})
    return render(response,"Emergency/emergencyPredict.html",{"minSave":min(job_loss),"maxSave":max(job_loss),"portfolio":False})
