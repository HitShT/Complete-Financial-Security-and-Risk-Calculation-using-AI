from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import os
from Base import gradeAndPredict
from Base.models import allPredictionsData,UserDependents,presentAssetsData
from django.contrib.auth.models import User
# Create your views here.
from .models import healthInsuranceSelected

def addAge(age):
    age = int(age)
    if age <= 30:
        return 30
    if age <= 45:
        return 45
    if age <= 60:
        return 60
    return 75

def multiplyList(mul,list):
    return [i*mul for i in list]

def sort_preferences(df,requests_form):
    cols = [i for i in df]
    for i in requests_form:
        try:
            requests_form[i] = int(requests_form[i])
        except:
            pass
    sm = requests_form["importance_premium"]+requests_form["importance_exclusion"]+requests_form["importance_noclaim"]+requests_form["importance_exhaustion"]+requests_form["importance_copay"]+requests_form["importance_claims"]+100
    requests_form["importance_premium"] /= sm
    requests_form["importance_exclusion"] /= sm
    requests_form["importance_noclaim"] /= sm
    requests_form["importance_exhaustion"] /= sm
    requests_form["importance_copay"] /= sm
    requests_form["importance_claims"] /= sm

    # print(requests_form["importance_premium"],requests_form["importance_exclusion"],requests_form["importance_noclaim"],requests_form["importance_exhaustion"],requests_form["importance_copay"],requests_form["importance_claims"],100/sm)

    #Getting the data
    company = list(df["Company"])
    plan = list(df["Plan"])
    premium = multiplyList(requests_form["importance_premium"],list(map(float,df["Premium"])))
    exclusionYears = multiplyList(requests_form["importance_exclusion"],list(map(float,df["Exclusion Years"])))
    sublimits = multiplyList(100/sm,list(map(float,df["Sublimits"])))
    noClaimBonus = multiplyList(requests_form["importance_noclaim"],list(map(float,df["No Claim Bonus"])))
    restoration = multiplyList(requests_form["importance_exhaustion"],list(map(float,df["restoration"])))
    copay = multiplyList(requests_form["importance_copay"],list(map(float,df["Co Pay"])))
    claimsSettled = multiplyList(requests_form["importance_claims"],list(map(float,df["Claims Settled"])))
    total_sum = [0]*len(premium)

    for i in range(len(premium)):
        total_sum[i] += premium[i] + exclusionYears[i] + sublimits[i] + noClaimBonus[i] + restoration[i] + copay[i] + claimsSettled[i]

    resp = {
        "Company":company,
        "Plan":plan,
        "Premium":premium,
        "Exclusion Years":exclusionYears,
        "Sublimits":sublimits,
        "No Claim Bonus":noClaimBonus,
        "restoration":restoration,
        "Co Pay":copay,
        "Claims Settled":claimsSettled,
        "Total Marks":total_sum,

        "prePremium":list(map(float,df["prePremium"])),
        "preExclusion Years":list(map(float,df["preExclusion Years"])),
        "preSublimits":list(df["preSublimits"]),
        "preNo Claim Bonus":list(map(float,df["preNo Claim Bonus"])),
        "prerestoration":list(df["prerestoration"]),
        "preCo Pay":list(df["preCo Pay"]),
        "preClaims Settled":list(map(float,df["preClaims Settled"])),
    }
    df = pd.DataFrame(data = resp)
    df = df.sort_values(by=["Total Marks"],ascending = False)
    # print(sublimits)
    return df

# TODO: Make a limit for the range of family policy, max of 45
def getData(response):
    if response.method == "POST":
        form_response = response.POST
        requests_form = {}
        requests_form["user_age"] = form_response["user_Age"]
        requests_form["policy_amount"] = form_response["Individual_policy_amount"]
        requests_form["importance_premium"] = form_response["valuePremium"]
        requests_form["importance_exclusion"] = form_response["valueExclusionYears"]
        requests_form["importance_noclaim"] = form_response["valueNoClaim"]
        requests_form["importance_exhaustion"] = form_response["count_exhaustion_choose"]
        requests_form["importance_copay"] = form_response["count_copay_choose"]
        requests_form["importance_claims"] = form_response["valueclaimsettled"]
        file_name = ""

        if(form_response["policy_type"] == "A"): #Individual policy
            if(addAge(requests_form["user_age"]) == 75):
                file_name += "Policies Insured Age "
            else:
                file_name += "Policies Single Age "
            file_name += str(addAge(requests_form["user_age"]))+" - Sum Insured = "+str(requests_form["policy_amount"]) + " lakh"

        else:
            requests_form["family_type"] = form_response["family_type_choose"]
            file_name += "Policies Family Insured "
            if(int(requests_form["user_age"]) <= 30):
                file_name += "30 "
            else:
                file_name += "45 "
            file_name += requests_form["family_type"]+" - Sum Insured = "+requests_form["policy_amount"]+" lakh"

        file_name += ".csv"
        # directory = os.getcwd()+r'Health Insurance\Graded Data'
        # directory = os.path.abspath(directory)
        directory = os.path.join(os.getcwd(),"HealthInsurancePredict")
        directory = os.path.join(directory,"Health Insurance")
        directory = os.path.join(directory,"Graded Data")
        file_name = os.path.join(directory,file_name)
        df = sort_preferences(pd.read_csv(file_name),requests_form)
        retDict = {
            "dataset":df.iterrows()
        }
        print(df)

        return render(response,"HealthInsurancePredict/getData.html",context = retDict)
    return render(response,"HealthInsurancePredict/getData.html")


def predictionData(response):
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

    rangeHealth = ob.range_health

    amount_health_present = max(0,presentInvestmentValue-highLiquid)

    categories = []
    typePolicy = ""
    data = []
    if(min(rangeHealth) > amount_health_present):
        form_response = response.POST
        if response.POST.get("press"):
            categories = [5,-1,-1,-1]
            mx = 0
            if 1000000 <= max(rangeHealth):
                categories[1] = 10
                mx = 1
            if 2000000 <= max(rangeHealth):
                categories[2] = 20
                mx = 2
            if 5000000 <= max(rangeHealth):
                categories[3] = 50
                mx = 3
            if form_response["type"] == "Single":
                typePolicy = form_response['type']
                return render(response, 'HealthInsurancePredict/predictionHealth.html',{"type":typePolicy,"amountMin":categories[0],"amountMax":categories[mx],"categories":categories,"chosen":False})
            else:
                return render(response, 'HealthInsurancePredict/predictionHealth.html',{"type":"Family","amountMin":categories[0],"amountMax":categories[mx],"categories":categories,"chosen":False})

        if response.POST.get("press2"):
            form_response = response.POST
            for i in ['5','10','20','50']:
                try:
                    categories.append(form_response[i])
                except:
                    continue
            fileName = ""
            if age <= 30:
                fileName = "Policies Single Age 30 - Sum Insured = "+form_response["amountInsurance"]+" lakh.csv"
            elif age <= 45:
                fileName = "Policies Single Age 45 - Sum Insured = "+form_response["amountInsurance"]+ "lakh.csv"
            elif age <= 60:
                fileName = "Policies Single Age 60 - Sum Insured = "+form_response["amountInsurance"]+ " lakh.csv"
            else:
                fileName = "Policies Insured Age 75 - Sum Insured = "+form_response["amountInsurance"]+ " lakh.csv"

            response.session["amountPolicy"] = form_response["amountInsurance"]

            prefix = "/Users/sd/Desktop/Capstone Project/CapstoneProject/HealthInsurancePredict/Health Insurance/Graded Data/"+fileName
            data = []
            try:
                file = pd.read_csv(prefix)
                data = []
                for index,row in file.iterrows():
                    temp = []
                    temp = [index+1,row["Company"],row["Plan"],row["prePremium"],row["preExclusion Years"],row["preSublimits"],row["preNo Claim Bonus"],row["prerestoration"],row["preCo Pay"],row["preClaims Settled"]]
                    temp = [str(i) for i in temp]
                    data.append(temp)
                response.session["healthDataset"] = data
                return render(response, 'HealthInsurancePredict/predictionHealth.html',{"type":"Single","amountMin":categories[0],"amountMax":categories[-1],"categories":categories,"chosen":form_response["amountInsurance"],"dataHealth":data})
            except Exception as e:
                print(e)
            return render(response, 'HealthInsurancePredict/predictionHealth.html',{"type":"Single","amountMin":categories[0],"amountMax":categories[-1],"categories":categories,"chosen":form_response["amountInsurance"]})

        if response.POST.get("press4"):
            form_response = response.POST
            for i in ['5','10','20','50']:
                try:
                    categories.append(form_response[i])
                except:
                    continue
            fileName = "Policies Family Insured " + form_response["familyType"] + " - Sum Insured = " + form_response["amountInsurance"] + " lakh.csv"

            response.session["amountPolicy"] = form_response["amountInsurance"]


            prefix = "/Users/sd/Desktop/Capstone Project/CapstoneProject/HealthInsurancePredict/Health Insurance/Graded Data/"+fileName
            data = []
            try:
                file = pd.read_csv(prefix)
                data = []
                for index,row in file.iterrows():
                    temp = []
                    temp = [index+1,row["Company"],row["Plan"],row["prePremium"],row["preExclusion Years"],row["preSublimits"],row["preNo Claim Bonus"],row["prerestoration"],row["preCo Pay"],row["preClaims Settled"]]
                    temp = [str(i) for i in temp]
                    data.append(temp)
                response.session["healthDataset"] = data
                return render(response, 'HealthInsurancePredict/predictionHealth.html',{"type":"Family","amountMin":categories[0],"amountMax":categories[-1],"categories":categories,"chosen":form_response["amountInsurance"],"dataHealth":data})
            except Exception as e:
                print(e)
            return render(response, 'HealthInsurancePredict/predictionHealth.html',{"type":"Family","amountMin":categories[0],"amountMax":categories[-1],"categories":categories,"chosen":form_response["amountInsurance"]})

        if response.POST.get("press3"):
            form_response = response.POST
            insurance = response.session["healthDataset"][int(form_response["selectedPolicy"])]
            healthInsuranceSelected(user=User.objects.get(username=response.user.username),plan = insurance[2],company = insurance[1],amount = int(response.session["amountPolicy"]),premium = int(float(insurance[3]))).save()
            return render(response, 'HealthInsurancePredict/predictionHealth.html')

    return render(response, 'HealthInsurancePredict/predictionHealth.html',{"type":False})
