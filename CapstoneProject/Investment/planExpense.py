import investmentPredictor

class planExpense:
    def __init__(self,amount,duration):
        self.amount = amount
        self.duration = duration
        self.ret = 8.5  # TODO: Calculate an average return
        self.retMonthly = self.convertYearlyMonthlyReturn(self.ret)
        self.monthlySave = self.amountMonthlySave(self.amount*1.2,self.retMonthly)
        # amount,risk,duration,liquidity
        self.portfolio = investmentPredictor.Investment(self.monthlySave,50,self.duration,0).portfolio

        for i in self.portfolio:
            self.portfolio[i] = self.portfolio[i][0]*self.portfolio[i][1]

        self.totalEquity = sum([self.portfolio[i] for i in self.portfolio])
        #Remaining is to be invested in safe deposits like bank
        self.totalInvestment = self.compoundInterest(self.totalEquity,self.duration,self.retMonthly)
        self.remaining = self.amount - self.totalInvestment

        if self.remaining > 0:
            self.portfolio["Savings"] = self.amountMonthlySave(self.remaining,self.convertYearlyMonthlyReturn(3))

        for i in self.portfolio:
            print("{} invest {}".format(i,self.portfolio[i]))

    def compoundInterest(self,amt,duration,ret):
        temp = (1+ret/100)
        ret = (temp**(duration-1)-1)/(temp-1)
        return ret*amt

    def convertYearlyMonthlyReturn(self,ret):
        temp = (1+ret/100)**(1/12)
        temp -= 1
        return temp*100

    def amountMonthlySave(self,amount,ret):
        # => x = y(r-1)/(r^d-1)
        #
        # r = (1+z/100)

        r = (1+ret/100)
        return amount*(r-1)/((r**(self.duration+1))-1)
