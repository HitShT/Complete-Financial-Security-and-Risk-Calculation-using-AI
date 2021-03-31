import pandas as pd

class Investment:
    def __init__(self,amount,risk,duration,liquidity):
        '''
            0 <= risk <= 100 *Done
            duration in months *Done
            0 <= liquidity <= 100
        '''
        self.amount = amount
        self.risk = risk
        self.duration = duration
        self.liquidity = liquidity
        self.stocksList = pd.read_csv("getMutualFunds\mfEquityDetails.csv")
        self.bondsList = pd.read_csv("getMutualFunds\mfBondDetails.csv")
        self.classEquityBonds()
        self.segregrateEquityBonds()
        self.getRequirements()
        self.printEquityChoices()

    def classEquityBonds(self):
        self.typeFundsEquity = {}
        self.typeBondsEquity = {}
        st = set()
        for i in list(self.stocksList["Type"]):
            for j in i.split(","):
                st.add(j)
        st2 = set()
        for i in list(self.bondsList["Type"]):
            for j in i.split(","):
                st2.add(j)
        for i in st:
            self.typeFundsEquity[i] = []
        for i in st2:
            self.typeBondsEquity[i] = []

    def segregrateEquityBonds(self):
        for i in range(len(self.stocksList["Type"])):
            temp = self.stocksList["Type"][i].split(",")
            for j in temp:
                add = [self.stocksList["Name"][i],self.stocksList["Number"][i],self.stocksList["Price"][i]]
                self.typeFundsEquity[j].append(add)

        for i in range(len(self.bondsList["Type"])):
            temp = self.bondsList["Type"][i].split(",")
            for j in temp:
                self.typeBondsEquity[j].append(self.bondsList["Name"][i])

    def getRequirements(self):
        self.investmentTypeDuration = None
        self.riskAcceptedStocks = {
            "Large Cap" : 30,
            "Mid" :20,
            'Small' :20,
        }
        self.bondsPercentage = 10

        if self.duration <= 6:
            self.investmentTypeDuration = "Ultra short duration"
        elif self.duration <= 12:
            self.investmentTypeDuration = "Low Duration"
        elif self.duration <= 36:
            self.investmentTypeDuration = "Short Duration"
        elif self.duration <= 48:
            self.investmentTypeDuration = "Medium Duration"
        elif self.duration <= 84:
            self.investmentTypeDuration = "Medium to Long Duration"
        else:
            self.investmentTypeDuration = "Long Duration"

        self.riskAcceptedStocks['Large Cap'] = 0.003*self.risk*self.risk-0.75*self.risk+60
        self.bondsPercentage = self.riskAcceptedStocks['Large Cap']/3
        self.riskAcceptedStocks["Mid"] = (100-self.riskAcceptedStocks['Large Cap']-self.bondsPercentage)/2
        self.riskAcceptedStocks["Small"] = self.riskAcceptedStocks["Mid"]

        self.bondsPercentage = self.liquidity

        tmp = self.riskAcceptedStocks["Large Cap"]+self.riskAcceptedStocks["Mid"]+self.riskAcceptedStocks['Small']
        self.riskAcceptedStocks["Large Cap"] /= tmp
        self.riskAcceptedStocks["Mid"] /= tmp
        self.riskAcceptedStocks["Small"] /= tmp

        tmp = 100-self.bondsPercentage
        self.riskAcceptedStocks["Large Cap"] *= tmp
        self.riskAcceptedStocks["Mid"] *= tmp
        self.riskAcceptedStocks["Small"] *= tmp

        self.amountLarge = self.amount*self.riskAcceptedStocks["Large Cap"]/100
        self.amountMid = self.amount*self.riskAcceptedStocks["Mid"]/100
        self.amountSmall = self.amount*self.riskAcceptedStocks["Small"]/100
        self.amountBonds =  self.amount*self.bondsPercentage/100

    def printEquityChoices(self):

        self.typeFundsEquity["Large Cap"].sort(key=lambda x: x[1])
        self.typeFundsEquity["Mid Cap"].sort(key=lambda x: x[1])
        self.typeFundsEquity["Focused"].sort(key=lambda x: x[1])
        self.typeFundsEquity["Small Cap"].sort(key=lambda x: x[1])
        self.typeFundsEquity["Value"].sort(key=lambda x: x[1])
        self.typeFundsEquity["Multi Cap"].sort(key=lambda x: x[1])
        self.typeFundsEquity["Contra"].sort(key=lambda x: x[1])
        self.typeFundsEquity["Large and Mid Cap"].sort(key=lambda x: x[1])

        
Investment(1000,73,120,40)
