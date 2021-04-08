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
        self.bondsList = pd.read_csv("getMutualFunds\corporateBondsDetails.csv")
        self.classEquityBonds()
        self.segregrateEquityBonds()
        self.getRequirements()
        self.printEquityChoices()

    def classEquityBonds(self):
        self.typeFundsEquity = {}
        self.typeBonds = {}
        st = set()
        for i in list(self.stocksList["Type"]):
            for j in i.split(","):
                st.add(j)

        for i in st:
            self.typeFundsEquity[i] = []

        durationsList = ['Return after 1 Year','Return after 3 Year','Return after 5 Year']

        durationBond = 0

        if self.duration < 12 :
            durationBond = 0
        elif self.duration < 36:
            durationBond = 1
        else:
            durationBond = 2

        for i in range(len(self.bondsList["Name"])):
            cp = 0
            for j in range(durationBond+1):
                if self.bondsList[durationsList[j]][i] != "-":
                    cp = j
            self.typeBonds[self.bondsList["Name"][i]] = [self.bondsList[durationsList[cp]][i],self.bondsList["Minimum SIP Amount"][i]]

    def segregrateEquityBonds(self):
        for i in range(len(self.stocksList["Type"])):
            temp = self.stocksList["Type"][i].split(",")
            for j in temp:
                add = [self.stocksList["Name"][i],self.stocksList["Number"][i],self.stocksList["Price"][i]]
                self.typeFundsEquity[j].append(add)

    def sorDict(self,dic):
        tmp = list(dic.values())
        tmp.sort()
        tmp = tmp[::-1]
        tmpp = {}

        for i in dic:
            tmpp[tuple(dic[i])] = i

        ret = {}
        for i in tmp:
            ret[tmpp[tuple(i)]] = i
        return ret

    def getRequirements(self):

        for i in self.typeBonds:
            if "%" in self.typeBonds[i][0]:
                self.typeBonds[i][0] = self.typeBonds[i][0][:-1]
            self.typeBonds[i][0] = float(self.typeBonds[i][0])

        # print(sorted(self.typeBonds.items(), key=lambda e: e[1][0]))

        self.typeBonds = self.sorDict(self.typeBonds)

        self.investmentTypeDuration = None
        self.riskAcceptedStocks = {
            "Large Cap" : 30,
            "Mid" :20,
            'Small' :20,
        }
        self.bondsPercentage = 10

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

        self.portfolio = {}

        i = 0
        while self.amountLarge > 0 and i < len(self.typeFundsEquity["Large Cap"]):
            if self.amountLarge > self.typeFundsEquity["Large Cap"][i][2]:
                self.portfolio[self.typeFundsEquity["Large Cap"][i][0]] = [self.amountLarge//self.typeFundsEquity["Large Cap"][i][2],self.typeFundsEquity["Large Cap"][i][2]]
                self.amountLarge = self.amountLarge - (self.amountLarge//self.typeFundsEquity["Large Cap"][i][2])*self.typeFundsEquity["Large Cap"][i][2]
            i += 1

        i = 0

        while self.amountMid > 0 and i < len(self.typeFundsEquity["Mid Cap"]):
            if self.amountMid > self.typeFundsEquity["Mid Cap"][i][2]:
                if self.typeFundsEquity["Mid Cap"][i][0] not in self.portfolio:
                    self.portfolio[self.typeFundsEquity["Mid Cap"][i][0]] = [self.amountMid//self.typeFundsEquity["Mid Cap"][i][2],self.typeFundsEquity["Mid Cap"][i][2]]
                    self.amountMid = self.amountMid - (self.amountMid//self.typeFundsEquity["Mid Cap"][i][2])*self.typeFundsEquity["Mid Cap"][i][2]
            i += 1

        i = 0

        while self.amountSmall > 0 and i < len(self.typeFundsEquity["Small Cap"]):
            if self.amountSmall > self.typeFundsEquity["Small Cap"][i][2]:
                if self.typeFundsEquity["Small Cap"][i][0] not in self.portfolio:
                    self.portfolio[self.typeFundsEquity["Small Cap"][i][0]] = [self.amountSmall//self.typeFundsEquity["Small Cap"][i][2],self.typeFundsEquity["Small Cap"][i][2]]
                    self.amountSmall = self.amountSmall - (self.amountSmall//self.typeFundsEquity["Small Cap"][i][2])*self.typeFundsEquity["Small Cap"][i][2]
            i += 1



        i = 0

        while self.amountBonds > 0 and i < len(self.typeBonds):

            if self.amountBonds > self.typeBonds[list(self.typeBonds.keys())[i]][1]:

                if self.typeBonds[list(self.typeBonds.keys())[i]][1] == 0:
                    self.portfolio[list(self.typeBonds.keys())[i]] = [self.amountBonds,self.typeBonds[list(self.typeBonds.keys())[i]][1]]
                    self.amountBonds = 0

                else:
                    self.portfolio[list(self.typeBonds.keys())[i]] = [(self.amountBonds//self.typeBonds[list(self.typeBonds.keys())[i]][1])*self.typeBonds[list(self.typeBonds.keys())[i]][1],self.typeBonds[list(self.typeBonds.keys())[i]][1]]

                    self.amountBonds = self.amountBonds -self.portfolio[list(self.typeBonds.keys())[i]][0]
            i += 1


        return self.portfolio


# for i in range(1000,20000):
#     for j in range(1,101):
#         for k in range(125):
#             for l in range(101):
#                 Investment(i,j,k,l)


class InvestmentMutualFunds:
    def __init__(self,amount,risk,duration,liquidity):
        '''
            If amount < 500, no MF, so suggest individual stocks
            if each individual < 500, join and SIP
        '''
        if(amount > 500):
            self.amount = amount
            self.risk = risk
            self.duration = duration
            self.liquidity = liquidity
            # TODO: Liquidity for bonds
            self.mfList = pd.read_csv("getMutualFunds\mutualFundReturns.csv")
            self.minSIP = 500
            self.classMF()
            self.getPercentageFunds()
            self.getChoices()
        else:
            print("Please invest in individual Stocks, no MF with minimum SIP amount")

    def classMF(self):
        self.nameMF,self.typeMF,self.returnMF = list(self.mfList["Name"]),list(self.mfList["Type"]),list(self.mfList["Average Return"])
        self.typeName = {i : [] for i in set(self.typeMF)}
        for i in range(len(self.nameMF)):
            self.typeName[self.typeMF[i]].append([self.nameMF[i],self.returnMF[i],500])
        for i in self.typeName:
            self.typeName[i].sort(key = lambda x : x[1],reverse = True)
        # print([i for i in self.typeName])

    def modify(self):
        if self.duration <= 6:
            temp = 0.001*self.risk*self.risk + 0.15*self.risk + 15
            self.midCap = temp
            self.smallCap = temp
            self.ultraShort = 4*(100-temp-temp)/5
            self.largeCap = (100-2*temp)/5


        elif self.duration <= 12:
            self.midCap = 0.2*self.risk + 10
            self.smallCap = 0.2*self.risk + 10
            rem = 100-2*self.midCap
            self.lowDuration = 2*rem/3
            self.focused = self.lowDuration/8
            self.largeCap = self.focused*3

        elif self.duration <= 36:
            self.smallCap = 0.002*self.risk*self.risk + 10
            self.midCap = self.smallCap
            rem = 100-2*self.midCap
            self.shortDuration = 4*rem/7
            self.value = self.shortDuration/8
            self.contra = self.value
            self.focused = self.value
            self.largeCap = 3*self.value

        elif self.duration <= 48:
            self.midCap = 0.003*self.risk*self.risk - 0.05*self.risk + 5
            self.smallCap = 0.003*self.risk*self.risk - 0.05*self.risk + 5
			rem = (100-2*self.midCap)
			self.medDuration = rem/2
			self.largeCap = 3*rem/16
            self.focused = rem/16
            self.liquid = rem/4

        elif self.duration <= 84:
			self.smallCap = 0.003*self.risk*self.risk - 0.05*self.risk + 5
			self.midCap = self.smallCap
			rem = 100 - 2*self.midCap
			self.medLongDuration = rem/2
			self.largeCap = self.medLongDuration/2
			self.liquid = self.largeCap/2

        else:
			self.midCap = 0.002*self.risk*self.risk + 0.1*self.risk + 5
			self.smallCap = self.midCap
			rem = 100 - 2*self.smallCap # 70
			self.longDuration = 4*rem/7
			self.liquid = rem/7
			self.focused = self.liquid/2
			self.largeCap = 3*self.focused

    def getPercentageFunds(self):

        self.largeCap = 0
        self.midCap = 0
        self.smallCap = 0
        self.value = 0
        self.contra = 0
        self.focused = 0
        self.longDuration = 0
        self.medDuration = 0
        self.medLongDuration = 0
        self.shortDuration = 0
        self.lowDuration = 0
        self.ultraShort = 0
        self.liquid = 0

        if self.duration <= 6:
            self.ultraShort = 40
            self.largeCap = 10
            self.midCap = 25
            self.smallCap = 25




        elif self.duration <= 12:
            self.lowDuration = 40
            self.largeCap = 15
            self.midCap = 20
            self.smallCap = 20
            self.focused = 5

        elif self.duration <= 36:
            self.shortDuration = 40
            self.largeCap = 15
            self.midCap = 15
            self.smallCap = 15
            self.value = 5
            self.contra = 5
            self.focused = 5

        elif self.duration <= 48:
            self.medDuration = 40
            self.largeCap = 15
            self.midCap = 10
            self.smallCap = 10
            self.focused = 5
            self.liquid = 10

        elif self.duration <= 84:
            self.medLongDuration = 40
            self.largeCap = 20
            self.midCap = 10
            self.smallCap = 10
            self.liquid = 10

        else:
            self.longDuration = 40
            self.largeCap = 15
            self.midCap = 15
            self.smallCap = 15
            self.focused = 5
            self.liquid = 10

        self.modify()

    def getChoices(self):

        self.largeCap *= self.amount/100
        self.midCap *= self.amount/100
        self.smallCap *= self.amount/100
        self.value *= self.amount/100
        self.contra *= self.amount/100
        self.focused *= self.amount/100
        self.longDuration *= self.amount/100
        self.medDuration *= self.amount/100
        self.medLongDuration *= self.amount/100
        self.shortDuration *= self.amount/100
        self.lowDuration *= self.amount/100
        self.ultraShort *= self.amount/100
        self.liquid *= self.amount/100

        self.portfolio = {}
        self.remaining = 0

        def addPortfolio(typeAmount,fundsType):
            if typeAmount < 500:
                self.remaining += typeAmount
                return
            if typeAmount >=3000:
                self.portfolio[fundsType[0][0]] = [fundsType[0][1],typeAmount/2]
                self.portfolio[fundsType[1][0]] = [fundsType[1][1],typeAmount*0.3]
                self.portfolio[fundsType[2][0]] = [fundsType[2][1],typeAmount*0.2]
            elif typeAmount >= 2000:
                self.portfolio[fundsType[0][0]] = [fundsType[0][1],typeAmount*5/8]
                self.portfolio[fundsType[1][0]] = [fundsType[1][1],typeAmount*3/8]
            else:
                self.portfolio[fundsType[0][0]] = [fundsType[0][1],typeAmount]

        addPortfolio(self.largeCap,self.typeName['Large Cap'])
        addPortfolio(self.midCap,self.typeName['Mid Cap'])
        addPortfolio(self.smallCap,self.typeName['Small Cap'])
        addPortfolio(self.value,self.typeName['Value'])
        addPortfolio(self.contra,self.typeName['Contra'])
        addPortfolio(self.focused,self.typeName['Focused'])
        addPortfolio(self.longDuration,self.typeName['Long Duration'])
        addPortfolio(self.medDuration,self.typeName['Medium Duration'])
        addPortfolio(self.medLongDuration,self.typeName['Medium to Long Duration'])
        addPortfolio(self.shortDuration,self.typeName['Short Duration'])
        addPortfolio(self.lowDuration,self.typeName['Low Duration'])
        addPortfolio(self.ultraShort,self.typeName['Ultra short duration'])
        addPortfolio(self.liquid,self.typeName['Liquid'])

        return self.portfolio







InvestmentMutualFunds(10000,10,20,10)
