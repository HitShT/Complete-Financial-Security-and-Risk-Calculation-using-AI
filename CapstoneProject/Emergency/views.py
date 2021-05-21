from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
# Create your views here.
from Base import gradeAndPredict
from Investment import planExpense
from Base.models import addUserExpense,addUserInvestment
import datetime

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
