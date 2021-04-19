from investmentPredictor import Investment,InvestmentMutualFunds

# def __init__(self,amount,risk,duration,liquidity):
#Investment
#InvestmentMutualFunds
class emergencyInvestment:
    def __init__(self,amount):
        self.amount = amount
        self.risk = 0
        self.duration = 2
        self.liquidity = 75
        # Equity by nature are completely liquid
        # TODO: design a way to remove bonds
        print(1,Investment(self.amount,self.risk,self.duration,0).portfolio)
        print(2,InvestmentMutualFunds(self.amount,self.risk,self.duration,self.liquidity).portfolio)


emergencyInvestment(10000)
