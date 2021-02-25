from django.shortcuts import render, redirect
from .forms import userLoginForm,Register,assetFormset,liabilitesFormset,dependentsFormset,userIncomeDataForm
from .models import presentAssetsData,presentLiabilitiesData,UserDependents,userIncomeData
from django.forms import formset_factory
from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
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

    return render(response, template_name, {
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

# @login_required
# def getAllData(response):
#     template_name = 'Base/tempDisplay.html'
#     assetData = presentAssetsData.objects.filter(user=User.objects.get(username=response.user.username))
#     context = {
#     "assetData":assetData
#     }
#     print(type(assetData))
#     return render(response,template_name,context)
