from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import os
# Create your views here.

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
    requests_form = {i:int(requests_form[i]) for i in requests_form}
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
        "Total Marks":total_sum
    }
    df = pd.DataFrame(data = resp)
    df = df.sort_values(by=["Total Marks"],ascending = False)
    print(sublimits)
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
        directory = os.path.abspath(r'C:\Users\Shashanka\Desktop\Capstone Project\CapstoneProject\HealthInsurancePredict\Health Insurance\Graded Data')
        file_name = os.path.join(directory,file_name)
        df = sort_preferences(pd.read_csv(file_name),requests_form)
        retDict = {
            "dataset":df.iterrows()
        }
        return render(response,"HealthInsurancePredict\getData.html",context = retDict)
    return render(response,"HealthInsurancePredict\getData.html")
