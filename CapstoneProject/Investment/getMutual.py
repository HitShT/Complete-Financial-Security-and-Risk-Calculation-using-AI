from requests import get
from bs4 import BeautifulSoup

url = ["https://www.moneycontrol.com/mutual-funds/canara-robeco-blue-chip-equity-fund-direct-plan/portfolio-holdings/MCA212","https://www.moneycontrol.com/mutual-funds/tata-income-fund-direct-plan/portfolio-debt/MTA755","https://www.moneycontrol.com/mutual-funds/canara-robeco-equity-hybrid-fund-direct-plan/portfolio-overview/MCA208","https://www.moneycontrol.com/mutual-funds/canara-robeco-blue-chip-equity-fund-regular-plan/portfolio-holdings/MCA174"]
percentage = [0,0] # equity and debt

def getStocksPercentage(soup):
    equity = soup.find(id = "equityCompleteHoldingTable")
    row = equity.find_all('tr')
    for index in range(1,len(row)):
        rowDetails = row[index].find_all("td")
        rowDetails = [i.text for i in rowDetails]
        for i in range(12):
            rowDetails[i] = rowDetails[i].replace("\n","")
        print(rowDetails[0],rowDetails[4])

def getDebtPercentage(soup):
    debt = soup.find(id = "portfolioDebtTable")
    row = debt.find_all("tr")
    for index in range(1,len(row)):
        rowDetails = row[index].find_all("td")
        rowDetails = [i.text for i in rowDetails]
        for i in range(8):
            rowDetails[i] = rowDetails[i].replace("\n","")
        if("Bond - Govt of India" not in rowDetails[0]): #Ignoring government of india bonds
            print(rowDetails[0],rowDetails[3],rowDetails[-2])

def getDivision(soup):
    test = soup.find_all("ul",{"class" : "nav-tabs mctab"})

    test = test[0].text.split("\n")
    test.pop(0)
    test.pop()
    test.pop()
    global percentage
    percentage = [0,0] #equity and debt
    for i in range(2):
        temp = test[i].split()
        percentage[i] = float(temp[1][1:-2])


for i in url:
    response = get(i)
    soup = BeautifulSoup(response.text, 'html.parser')

    getDivision(soup)

    if(percentage[0] > 0):
        getStocksPercentage(soup)
    if(percentage[1] > 0):
        getDebtPercentage(soup)
