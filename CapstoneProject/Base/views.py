from django.shortcuts import render, redirect
from .forms import userLoginForm,Register,assetFormset,liabilitesFormset,dependentsFormset,userIncomeDataForm,userExpenseFormset,userInvestmentFormset,allPredictionsDataForm
from .models import presentAssetsData,presentLiabilitiesData,UserDependents,userIncomeData,addUserExpense,addUserInvestment,allPredictionsData
from django.forms import formset_factory
from django.contrib.auth.models import User
from Investment.models import investmentAreas,investmentDivision

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
# Create your views here.

def userLogin(response):
    userLoginDetails = userLoginForm()
    if response.method == "POST":
        username,password = response.POST.get("username"),response.POST.get("password")
        user =  authenticate(username = username,password = password)
        if not user:
            return render(response,"Base/login.html",context = {"userLoginDetails":userLoginDetails})
        elif user.is_active:
            login(response,user)
            return redirect('/base/getUserAssets')
        else:
            return redirect('/base/login')
    return render(response,"Base/login.html",context = {"userLoginDetails":userLoginDetails})

@login_required
def userLogout(request):
    logout(request)
    return redirect('/base/login')

def check(response):
    return HttpResponse(response.user.is_authenticated)

def userRegister(response):
    template_name = 'Base/Register.html'
    if response.method == 'GET':
        registerForm = Register()
    elif response.method == 'POST':
        registerForm = Register(data =  response.POST)
        if registerForm.is_valid():
            registerFormObject = registerForm.save()
            registerFormObject.set_password(registerFormObject.password)
            registerFormObject.save()
            return redirect('/base/login')
    return render(response, 'Base/Register.html', {
        "RegisterForm":registerForm,
    })

@login_required
def getUserAssets(response):
    template_name = 'Base/addAssets.html'
    if response.method == 'GET':
        assetFormsetData = assetFormset(queryset=presentAssetsData.objects.none())
    elif response.method == 'POST':
        assetFormsetData = assetFormset(data = response.POST)
        if assetFormsetData.is_valid():
            for form in assetFormsetData:
                formObject = form.save(commit = False)
                formObject.user = User.objects.get(username=response.user.username)
                formObject.save()

    return render(response, template_name, {
        'assetFormsetData': assetFormsetData
    })

@login_required
def getUserLiabilities(response):
    template_name = 'Base/addLiabilities.html'
    if response.method == 'GET':
        liabilitiesFormsetData = liabilitesFormset(queryset=presentLiabilitiesData.objects.none())
    elif response.method == 'POST':
        liabilitiesFormsetData = liabilitesFormset(data = response.POST)
        if liabilitiesFormsetData.is_valid():
            for form in liabilitiesFormsetData:
                formObject = form.save(commit = False)
                formObject.user = User.objects.get(username=response.user.username)
                formObject.save()

    return render(response, template_name, context = {
        'liabilitiesFormsetData': liabilitiesFormsetData
    })

@login_required
def getUserDependents(response):
    template_name = 'Base/addDependents.html'
    if response.method == 'GET':
        dependentsFormsetData = dependentsFormset(queryset=UserDependents.objects.none())
    elif response.method == 'POST':
        dependentsFormsetData = dependentsFormset(data = response.POST)
        if dependentsFormsetData.is_valid():
            for form in dependentsFormsetData:
                formObject = form.save(commit = False)
                formObject.user = User.objects.get(username=response.user.username)
                formObject.save()

    return render(response, template_name, {
        'dependentsFormsetData': dependentsFormsetData
    })

@login_required
def getUserIncomeData(response):
    template_name = 'Base/addIncome.html'
    if response.method == 'GET':
        getIncome = userIncomeDataForm()
    elif response.method == 'POST':
        getIncome = userIncomeDataForm(data =  response.POST)
        if getIncome.is_valid():
            getIncomeObject = getIncome.save(commit = False)
            getIncomeObject.user = User.objects.get(username=response.user.username)
            getIncomeObject.save()
    return render(response, template_name, {
        "getIncome":getIncome,
    })

@login_required
def getUserExpenseData(response):
    template_name = "Base/addExpense.html"
    if response.method == "GET":
        userExpenseFormsetData = userExpenseFormset(queryset=addUserExpense.objects.none())
    elif response.method == "POST":
        userExpenseFormsetData = userExpenseFormset(data = response.POST)
        if userExpenseFormsetData.is_valid():
            for form in userExpenseFormsetData:
                formObject = form.save(commit = False)
                formObject.user = User.objects.get(username=response.user.username)
                formObject.save()
    return render(response,template_name, context = {
        "userExpenseFormsetData":userExpenseFormsetData
    })

@login_required
def getUserInvestmentData(response):
    template_name = "Base/addInvestment.html"
    if response.method == "GET":
        userInvestmentFormsetData = userInvestmentFormset(queryset=addUserInvestment.objects.none())
    elif response.method == "POST":
        userInvestmentFormsetData = userInvestmentFormset(data = response.POST)
        if userInvestmentFormsetData.is_valid():
            for form in userInvestmentFormsetData:
                formObject = form.save(commit = False)
                formObject.user = User.objects.get(username=response.user.username)
                formObject.save()
    return render(response,template_name, context = {
        "userInvestmentFormsetData":userInvestmentFormsetData
    })

@login_required
def getUserPredictionValues(response):
    #monthly salary, expense, yearly expense, age, dependents, presentInvestmentValue, investmentMonthly, investmentRate, health insurance value, future dependents
    monthly_salary1 = userIncomeData.objects.filter(user=User.objects.get(username=response.user.username))
    temp = 0
    for i in monthly_salary1:
        temp += i.fixed_salary + i.variable_salary_min
    monthly_salary1 = temp
    investment = addUserInvestment.objects.filter(user=User.objects.get(username=response.user.username))
    previousInvestment,monthlyInvestment = 0,0
    for i in investment:
        if i.investment_repeat_frequency <= 1: #one time investment
            previousInvestment += i.investment_amount
        else:
            monthlyInvestment += i.investment_amount
    expense = addUserExpense.objects.filter(user=User.objects.get(username=response.user.username))
    expense_yearly,expense_monthly = 0,0
    for i in expense:
        expense_yearly += i.expense_repeat_frequency*i.expense_amount
        if i.expense_repeat_frequency == 12:
            expense_monthly = i.expense_amount
    dependents = UserDependents.objects.filter(user=User.objects.get(username=response.user.username))
    dependentsCount = len([i for i in dependents])


    template_name = 'Base/getPredictionData.html'
    if response.method == 'GET':
        predictionsData = allPredictionsDataForm()
    elif response.method == 'POST':
        predictionsData = allPredictionsDataForm(data =  response.POST)
        if predictionsData.is_valid():
            predictionsDataObject = predictionsData.save(commit = False)
            predictionsDataObject.user = User.objects.get(username=response.user.username)
            predictionsDataObject.monthly_salary = monthly_salary1
            predictionsDataObject.investmentTotal = previousInvestment
            predictionsDataObject.investmentMonthly = monthlyInvestment
            predictionsDataObject.yearly_expense = expense_yearly
            predictionsDataObject.monthly_expense = expense_monthly
            predictionsDataObject.dependents = dependentsCount
            predictionsDataObject.healthInsurance = 0
            predictionsDataObject.save()
    return render(response, template_name, {
        "predictionsData":predictionsData
    })


@login_required
def showBuckets(response):
    #  buckets : health insurance, investment, saving for emergency
    # options : modify data

    linkHealth,linkInvestment,linkEmergency = "healthInsurance/predictionData","investment/decideType","emergency/saveAmount"



    if response.method == 'POST':
        if "investmentButton" in response.POST:
            return redirect("../"+linkInvestment)
        if "healthButton" in response.POST:
            return redirect("../"+linkHealth)
        if "emergencyButton" in response.POST:
            return redirect("../"+linkEmergency)

    return render(response,"Base/displayBoxes.html")
# @login_required
# def getAllData(response):
#     template_name = 'Base/tempDisplay.html'
#     assetData = presentAssetsData.objects.filter(user=User.objects.get(username=response.user.username))
#     context = {
#     "assetData":assetData
#     }
#     print(type(assetData))
#     return render(response,template_name,context)

@login_required
def financialOverview(response):
    userObject = User.objects.get(username=response.user.username)
    ob1 = investmentAreas.objects.filter(user = userObject)
    ob2 = investmentDivision.objects.filter(user = userObject)

    investmentName,investmentQuantity,investmentAmount = [],[],[]
    investmentType,investmentPercentage = [],[]

    investmentName = [i.investmentName for i in ob1]
    investmentQuantity = [i.investmentQuantity for i in ob1]
    investmentAmount = [i.investmentAmount for i in ob1]

    investmentType = [i.investmentType for i in ob2]
    investmentPercentage = [i.investmentPercentage for i in ob2]


    return render(response,"Base/overview.html",{"investmentType":investmentType,"investmentPercentage":investmentPercentage})
