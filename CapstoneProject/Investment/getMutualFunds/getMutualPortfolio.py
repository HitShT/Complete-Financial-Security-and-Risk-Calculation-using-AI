from requests import get
from bs4 import BeautifulSoup


#use lxml parser instead of lxml for much faster scraping

class getPortfolio:

    def __init__(self):
        self.percentage = [0,0]
        import pandas as pd
        self.df = pd.read_csv("mutualFundLinks.csv")
        self.url = self.df["Link"]
        # self.url = ["https://www.moneycontrol.com/mutual-funds/canara-robeco-blue-chip-equity-fund-direct-plan/portfolio-holdings/MCA212"]

        self.equityDetails = {}
        self.debtDetails = {}
        self.countIterations = 1

        for i in self.url:
            print("Started {} of {}".format(self.countIterations,len(self.url)))
            self.response = get(i)
            self.soup = BeautifulSoup(self.response.text, 'lxml')
            self.getDivision()
            if(self.percentage[0] > 0):
                self.getStocksPercentage()
            if(self.percentage[1] > 0):
                self.getDebtPercentage()

            print("Done {} of {}".format(self.countIterations,len(self.url)))
            self.countIterations += 1
        self.createCSVEquity()
        self.createCSVDebt()

    def getDivision(self):
        self.test = self.soup.find_all("ul",{"class" : "nav-tabs mctab"})
        self.test = self.test[0].text.split("\n")
        self.test.pop(0)
        self.test.pop()
        self.test.pop()
        self.percentage = [0,0] #equity and debt
        for i in range(2):
            self.temp = self.test[i].split()
            self.percentage[i] = float(self.temp[1][1:-2])

    def clean_name(self,name):
        self.updated = ""
        self.accepted = "qwertyuiopasdfghjklzxcvbnm 1234567890"
        for i in name:
            if i.lower() in self.accepted:
                self.updated += i
        return self.updated

    def getStockPrice(self,link_share):
        try:
            link_share = link_share[0]
            shareURL = link_share.find("a").get("href")
            shareResponse = get(shareURL)
            sharesoup = BeautifulSoup(shareResponse.text,"lxml")
            valueStock = sharesoup.find("input",{"id":"nprevclose"})
            return float(valueStock.get("value"))
        except:
            return -1

    def getStocksPercentage(self):
        self.equity = self.soup.find(id = "equityCompleteHoldingTable")
        self.row = self.equity.find_all('tr')
        for index in range(1,len(self.row)):
            self.rowDetails = self.row[index].find_all("td")
            self.rowDetails = [i.text for i in self.rowDetails]
            for i in range(12):
                self.rowDetails[i] = self.rowDetails[i].replace("\n","")

            self.stock_name = self.clean_name(self.rowDetails[0].strip())
            self.stock_percentage = self.rowDetails[4]
            self.stock_percentage = self.stock_percentage.strip()
            self.stock_percentage = float(self.stock_percentage.replace("%",""))
            self.stock_price = self.getStockPrice(self.row[index].find_all("td"))

            if(self.stock_name in self.equityDetails):
                self.equityDetails[self.stock_name][0] += self.stock_percentage
            else:
                self.equityDetails[self.stock_name] = [self.stock_percentage,self.stock_price]

    def getDebtPercentage(self):
        self.debt = self.soup.find(id = "portfolioDebtTable")
        self.row = self.debt.find_all("tr")
        for index in range(1,len(self.row)):
            self.rowDetails = self.row[index].find_all("td")
            self.rowDetails = [i.text for i in self.rowDetails]
            for i in range(8):
                self.rowDetails[i] = self.rowDetails[i].replace("\n","")
            self.bond_name = self.clean_name(self.rowDetails[0].strip())
            self.bond_name = self.bond_name.replace("Bond  ","")
            self.bond_percentage = self.rowDetails[-2].strip()
            self.bond_percentage = float(self.bond_percentage.replace("%",""))
            self.bond_rating = self.rowDetails[3].strip()
            if self.bond_name not in self.debtDetails:
                self.debtDetails[self.bond_name] = [self.bond_rating,self.bond_percentage]
            else:
                self.debtDetails[self.bond_name][1] += self.bond_percentage

    def createCSVEquity(self):
        self.name = []
        self.number = []
        self.price = []

        for i in self.equityDetails:
            self.name.append(i)
            self.number.append(self.equityDetails[i][0])
            self.price.append(self.equityDetails[i][1])
        import pandas as pd

        resp = {
            "Name":self.name,
            "Number":self.number,
            "Price":self.price
        }

        self.df = pd.DataFrame(data = resp)
        self.df.to_csv("mfEquityDetails.csv",sep=',',index=False)

    def createCSVDebt(self):
        self.name = []
        self.number = []
        self.rating = []

        for i in self.debtDetails:
            self.name.append(i)
            self.number.append(self.debtDetails[i][1])
            self.rating.append(self.debtDetails[i][0])
        import pandas as pd

        resp = {
            "Name":self.name,
            "Rating":self.rating,
            "Number":self.number
        }

        self.df = pd.DataFrame(data = resp)
        self.df.to_csv("mfBondDetails.csv",sep=',',index=False)

getPortfolio()
