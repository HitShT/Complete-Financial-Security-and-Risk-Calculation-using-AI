from django.shortcuts import render
from django.http import HttpResponse

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
    return HttpResponse("None")
