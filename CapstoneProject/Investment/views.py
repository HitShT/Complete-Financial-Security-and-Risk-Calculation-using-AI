from django.shortcuts import render
from django.http import HttpResponse
from Base import gradeAndPredict
from Base.models import allPredictionsData,UserDependents,presentAssetsData
from django.contrib.auth.models import User
from Investment import investmentPredictor
from .models import investmentAreas,investmentDivision,investmentRiskLiquidity
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

def combine(dic1,dic2):
    ret = {}
    for i in dic1:
        ret[i] = dic1[i]
    for i in dic2:
        if i not in ret:
            ret[i] = dic2[i]
        else:
            for i in range(len(ret[i])):
                ret[i] += dic2[i]
    return ret

def updateChanges(name,qty,data):
    dic_old = {name[i]:qty[i] for i in range(len(name))}
    dic_new = {i[0]:i[2] for i in data}
    print(dic_old)
    print(dic_new)
    dic_change = {}
    for i in dic_old:
        dic_change[i] = -dic_old[i]
    for i in dic_new:
        if i in dic_change:
            dic_change[i] += dic_new[i]
        else:
            dic_change[i] = dic_new[i]
    temp = []
    names = [i for i in dic_change]
    for i in range(len(names)):
        tp = [i+1,names[i],round(dic_change[names[i]],2)]
        temp.append(tp)
    return temp

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

    retirementSave = ob.retirementSave

    amount_retirement_present = max(0,presentInvestmentValue-highLiquid)

    check = False
    data = {}
    sm = 0
    updatedData = []
    if(max(retirementSave) > amount_retirement_present):
        if response.method == "POST":
            form_response = response.POST
            if response.POST.get("press"):
                # print(form.cleaned_data['risk'],form.cleaned_data['liquidity'])

                percentage_equity = int(form_response["percentage"])


                amount = max(retirementSave)-amount_retirement_present
                amount_equity = amount*percentage_equity/100
                amount_mutual = amount*(100-percentage_equity)/100

                ob = investmentPredictor.Investment(amount_equity,int(form_response['risk']),(60-age)*12,int(form_response['liquidity']))
                data = ob.portfolio

                amount_total_equity = amount_equity

                ob = investmentPredictor.InvestmentMutualFunds(amount_mutual,int(form_response['risk']),(60-age)*12,int(form_response['liquidity']))
                data2 = ob.portfolio

                for i in data2:
                    data2[i] = [round(data2[i][1],2),500]

                amount_total_mutual = amount_mutual

                data = combine(data,data2)

                ct = 1
                ls = []

                for i in data:
                    data[i] = [ct]+data[i]
                    ct += 1
                    if "Fund" not in i and "Plan" not in i:
                        data[i] = data[i] + [round(data[i][-1]*data[i][-2],2)]
                    else:
                        data[i] = data[i] + [round(data[i][-2],2)]
                    tp = [i]
                    for j in data[i]:
                        tp.append(j)
                    ls.append(tp)

                data = ls.copy()

                for i in range(len(data)):
                    sm += data[i][-1]
                    data[i][-2] = round(data[i][-2],2)
                    if(data[i][-2] == 0):
                        data[i][-1] = round(data[i][-3],2)
                        data[i][-3] = round(data[i][-3],2)

                amount_total_ETF = 0
                if(amount - sm >= 500):
                    amount_total_ETF = round(amount-sm,2)
                    temp = ["SENSEX ETF",data[-1][1]+1,round(amount-sm,2),500,round(amount-sm,2)]
                    sm += round(amount-sm,2)
                    data.append(temp)
                check = True


                userObject = User.objects.get(username=response.user.username)

                save1 = investmentAreas.objects.filter(user = userObject)
                save2 = investmentDivision.objects.filter(user = userObject)

                previousInvestmentName,previousInvestmentQuantity,previousInvestmentAmount = [i.investmentName for i in save1],[i.investmentQuantity for i in save1],[i.investmentAmount for i in save1]
                # previousInvestmentType,previousInvestmentPercentage = [i.investmentType for i in save2],[i.investmentPercentage for i in save2]

                updatedData = updateChanges(previousInvestmentName,previousInvestmentQuantity,data)

                save1.delete()
                save2.delete()
                #before adding, delete if there are old data
                for i in data:
                    ob = investmentAreas(user = userObject,investmentName = i[0],investmentQuantity = i[2],investmentAmount = i[3])
                    ob.save()

                investmentDivision(user = userObject,investmentType = "Equity",investmentPercentage = round((amount_total_equity*100)/(amount_total_equity+amount_total_ETF+amount_total_mutual),2)).save()
                investmentDivision(user = userObject,investmentType = "MF",investmentPercentage = round((amount_total_mutual*100)/(amount_total_equity+amount_total_ETF+amount_total_mutual),2)).save()
                investmentDivision(user = userObject,investmentType = "ETF",investmentPercentage = round((amount_total_ETF*100)/(amount_total_equity+amount_total_ETF+amount_total_mutual),2)).save()

                investmentRiskLiquidity(user = userObject,risk = form_response['risk'],liquidity = form_response['liquidity']).save()

        # ob = investmentPredictor.Investment()
        return render(response, 'Investment/predictionInvestment.html', {'check':check,'data':data,'amount':round((max(retirementSave)-amount_retirement_present),2),"sum":round(sm,2),"updatedData":updatedData})
    return HttpResponse(str(amount_retirement_present))
