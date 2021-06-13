import pickle
import pandas as pd
import random


class HealthPredict:
  def __init__(self,amount_remaining,monthly_income,age,dependents):
    self.amount_remaining = amount_remaining
    self.age = age
    if self.age <= 30:
      self.age = 30
    elif self.age <= 45:
      self.age = 45
    elif self.age <= 60:
      self.age = 60
    else:
      self.age = 75
    self.dependents = dependents
    self.monthly_income = monthly_income
    self.inflation = 13
    self.allHealth = pd.read_csv("Base/combinedHealth.csv")
  def getAmount(self,monthly_income):
    return 0.5*monthly_income*12
  def adjustForInflation(self):
    self.amountInsurance = self.getAmount(self.monthly_income)
    ret = (1+self.inflation/100)**((60-self.age)/2)
    return self.amountInsurance*ret
  def getHealthInsuranceAmount(self):
    ncb = [0,25,50,100]
    amt = self.adjustForInflation()
    return [amt,amt*4/5,amt*2/3,amt/2]
  def getPolicy(self):

    self.allHealth = self.allHealth[self.allHealth.prePremium <= self.amount_remaining]
    self.allHealth = self.allHealth[self.allHealth.Age == self.age]
    dep = "1A"
    if self.dependents:
      dep = input("What type of dependents do you have? Format 1A,2A 1C,2A 2C")
    self.allHealth = self.allHealth[self.allHealth.Type == dep]
    self.allHealth = self.allHealth.reset_index(drop = True)
    #Choose the policy, using a form Django
    #Choosing randomly here
    self.policyChoice = self.allHealth.iloc[random.randrange(0,len(self.allHealth["Plan"]))]
    return self.policyChoice #pandas DataFrame of chosen policy

class getPresentData:
  def __init__(self,monthly_salary,monthly_expense,expenses_yearly,age,dependents,presentInvestmentValue,presentInvestmentMonthly,presentInvestmentRate,presentHealthInsuranceValue,futureDependents):
    self.salary = monthly_salary
    self.salary_yearly = self.salary*12
    self.expenses_yearly = expenses_yearly
    self.age = age
    self.dependents = dependents
    self.presentInvestmentValue = presentInvestmentValue
    self.presentInvestmentRate = presentInvestmentRate
    self.presentInvestmentMonthly = presentInvestmentMonthly
    self.presentHealthInsuranceValue = presentHealthInsuranceValue
    self.monthly_expense = monthly_expense

class predictData(getPresentData):
  def __init__(self,monthly_salary,monthly_expense,expenses_yearly,age,dependents,presentInvestmentValue,presentInvestmentMonthly,presentInvestmentRate,presentHealthInsuranceValue,futureDependents):
    super().__init__(monthly_salary,monthly_expense,expenses_yearly,age,dependents,presentInvestmentValue,presentInvestmentMonthly,presentInvestmentRate,presentHealthInsuranceValue,futureDependents)
    self.files_models = [
        "Base/total_amount_elastic.sav",
        "Base/total_amount_lasso.sav",
        "Base/total_amount_ridge.sav",
        "Base/job_loss_random_forest.sav"
    ]
    self.total_amount_elastic = pickle.load(open(self.files_models[0], 'rb'))
    self.total_amount_lasso = pickle.load(open(self.files_models[1], 'rb'))
    self.total_amount_ridge = pickle.load(open(self.files_models[2], 'rb'))
    self.job_loss_random_forest = pickle.load(open(self.files_models[3], 'rb'))
    self.futureDependents = futureDependents
  def adjustInflation(self,amount):
    self.rate = 6
    ret = (1+self.rate/100)**(60-self.age)
    return amount*ret
  def getAmountTotalAmount(self):
    self.amount_required_monthly = self.monthly_expense
    if self.futureDependents:
      self.amount_required_monthly = self.monthly_expense*(1+self.futureDependents)*0.7
    self.retirement_monthly_amount = 0.7*self.adjustInflation(self.amount_required_monthly)
    self.retirement_yearly = self.retirement_monthly_amount*12
    return max(18*self.retirement_yearly-self.presentInvestmentValue,0)
  def getAmountTotalAmountGradingTheoretical(self):
    self.amount_required_monthly = self.monthly_expense
    if self.futureDependents:
      self.amount_required_monthly = self.monthly_expense*(1+self.futureDependents)*0.7
    self.retirement_monthly_amount = 0.7*self.adjustInflation(self.amount_required_monthly)
    self.retirement_yearly = self.retirement_monthly_amount*12
    return 18*self.retirement_yearly
  def convertYearlyMonthly(self,rate):
    monthly_rate = (1+rate/100)**(1/12)
    monthly_rate = (monthly_rate - 1)*100
    return round(monthly_rate,2)
  def theoreticalAmountMonthly(self):
    ret = 10
    self.monthly_rate = self.convertYearlyMonthly(ret)
    self.total_months = 60-self.age
    P = (1+self.monthly_rate/100)
    ret = P**(1+(60-self.age)*12)
    ret -= 1
    ret /= (P-1)
    return self.getAmountTotalAmount()/ret
  def predictAmountMonthly(self):
    X = [self.salary,self.monthly_expense,self.dependents,self.getAmountTotalAmount(),self.presentHealthInsuranceValue,60-self.age-1]
    pred = self.total_amount_ridge.predict([X])
    return pred[0]
  def jobLossTheoretical(self):
    # save 6-12 months. Assuming 3 months pay when job loss, 6+3 = 9 months
    return self.monthly_expense*6
  def jobLossPredict(self):
    X = [self.salary,self.monthly_expense,self.dependents,self.presentInvestmentValue]
    pred = self.job_loss_random_forest.predict([X])
    return pred[0]
  def healthInsuranceAmount(self):
    amount_remaining = self.salary*12-self.expenses_yearly-(self.monthly_expense)*12
    ob = HealthPredict(amount_remaining,self.salary,self.age,self.dependents)
    return ob.getHealthInsuranceAmount()

class GetAndPredict(predictData):
  def __init__(self,monthly_salary,monthly_expense,expenses_yearly,age,dependents,presentInvestmentValue,presentInvestmentMonthly,presentInvestmentRate,presentHealthInsuranceValue,futureDependents,healthInsurancePremium):
    super().__init__(monthly_salary,monthly_expense,expenses_yearly,age,dependents,presentInvestmentValue,presentInvestmentMonthly,presentInvestmentRate,presentHealthInsuranceValue,futureDependents)
    self.range_health = [min(self.healthInsuranceAmount()),max(self.healthInsuranceAmount())]
    self.job_loss = [min(self.jobLossPredict(),self.jobLossTheoretical()),max(self.jobLossPredict(),self.jobLossTheoretical())]
    self.retirementSave = [min(self.predictAmountMonthly(),self.theoreticalAmountMonthly()),max(self.predictAmountMonthly(),self.theoreticalAmountMonthly())]
    self.totalJobLoss = self.job_loss.copy()
    self.job_loss = [self.convertMonthly(self.job_loss[0]),self.convertMonthly(self.job_loss[1])]
    self.healthInsurancePremium = healthInsurancePremium
  def convertYearlyMonthlyReturn(self,ret):
    temp = (1+ret/100)**(1/12)
    temp -= 1
    return temp*100
  def amountMonthlySave(self,amount,ret,duration):
    r = (1+ret/100)
    return amount*(r-1)/((r**(duration+1))-1)
  def convertMonthly(self,amount):
    duration = 12
    rate = self.convertYearlyMonthlyReturn(7)
    return self.amountMonthlySave(amount,rate,duration)
  def absoluteChoices(self):
    print("Health Insurance Amount",min(self.healthInsuranceAmount()),"to",max(self.healthInsuranceAmount()))
    print("Total Amount to Save for Job Loss",min(self.job_loss),"to",max(self.job_loss))
    print("Amount to save monthly for retirements",min(self.predictAmountMonthly(),self.theoreticalAmountMonthly()),"to",max(self.predictAmountMonthly(),self.theoreticalAmountMonthly()))

  def healthInsurancePredictAmount(self):
    if self.yearlyRemaining:
      if self.presentHealthInsuranceValue >= self.range_health[0]:
        print("Health Insurance is covered")
      else:
        print("Consider upgrading Health Insurance")
        self.yearlyRemaining += self.healthInsurancePremium
        self.healthObject = HealthPredict(self.yearlyRemaining,self.salary,self.age,self.dependents)
        self.healthObject = self.healthObject.getPolicy()
        self.yearlyRemaining -= float(self.healthObject["prePremium"])
        healthOb = HealthPredict(self.yearlyRemaining,self.salary,self.age,self.dependents)
        self.policyChosen = healthOb.getPolicy()
        # print(self.policyChosen)
        self.yearlyRemaining -= self.policyChosen["prePremium"]

        #predict based on remaining yearly money
  def jobLossPredictAmount(self):
      if self.yearlyRemaining:
        if self.highLiquid >= self.job_loss[0]:
          print("Present investments of liquid assets is enough")
        else:
          # predict based on remaining money
          # subtract from remaining
          print("Consider upgrading amount saved for emergencies")
          if max(self.job_loss)*12 < self.yearlyRemaining:
            print("Consider saving between",min(self.job_loss),"and",max(self.job_loss))
            self.job_loss_saving = float(input("How much do you want to save?"))
            while self.job_loss_saving < min(self.job_loss) and self.job_loss_saving*12 < self.yearlyRemaining:
              self.job_loss_saving = float(input("How much do you want to save?"))
          else:
            if min(self.job_loss)*12 > self.yearlyRemaining:
              print("Consider investing everything to save for emergency")
              self.job_loss_saving = self.yearlyRemaining/12
            else:
              print("Consider saving between",min(self.job_loss),"and",self.yearlyRemaining/12)
              self.job_loss_saving = float(input("How much do you want to save?"))
              while self.job_loss_saving < min(self.job_loss) and self.job_loss_saving*12 < self.yearlyRemaining:
                self.job_loss_saving = float(input("How much do you want to save?"))
          self.yearlyRemaining -= self.job_loss_saving*12
  def retirementPredictAmount(self):
    if self.yearlyRemaining:
      if self.presentInvestmentValue >= self.retirementSave[0]:
        print("Present investment value is enough")
      else:
        # predict based on remaining money
        # subtract from remaining
        self.yearlyRemaining -= 0
        print("Consider upgrading amount saved for  retirement")
  def choicesBasedSituation(self):
    self.yearlyRemaining = 12*(self.salary-self.monthly_expense)-self.expenses_yearly

    for i in self.order:
      # ["Health","Job Loss","Total"]
      if i == "Health":
        self.healthInsurancePredictAmount()
      elif i == "Job Loss":
        self.jobLossPredictAmount()
      else:
        self.retirementPredictAmount()
      print("Remaining Money left to invest",self.yearlyRemaining)

class gradeExisting(GetAndPredict):
  def __init__(self,monthly_salary,monthly_expense,expenses_yearly,age,dependents,presentInvestmentValue,presentInvestmentMonthly,presentInvestmentRate,presentHealthInsuranceValue,futureDependents,highLiquid,healthInsurancePremium):
    super().__init__(monthly_salary,monthly_expense,expenses_yearly,age,dependents,presentInvestmentValue,presentInvestmentMonthly,presentInvestmentRate,presentHealthInsuranceValue,futureDependents,healthInsurancePremium)
    self.highLiquid = highLiquid
    self.gradeHealth = self.gradeHealthIns()
    self.gradeJobLoss = self.gradeTotalJobLoss()
    self.gradeTotal = self.gradeTotalAmount()
    self.gradeAll()
  def theoreticalAmountMonthlyTest(self,amt):
    ret = 10
    self.monthly_rate = self.convertYearlyMonthly(ret)
    self.total_months = 60-self.age
    P = (1+self.monthly_rate/100)
    ret = P**(1+(60-self.age)*12)
    ret -= 1
    ret /= (P-1)
    return min(1,amt/ret)
  def gradeTotalAmount(self):
    remainingAmount = self.getAmountTotalAmountGradingTheoretical()-self.presentInvestmentValue
    X = [self.salary,self.monthly_expense,self.dependents,remainingAmount,self.presentHealthInsuranceValue,60-self.age-1]
    pred = self.total_amount_ridge.predict([X])
    pred = pred[0]
    pred2 = self.theoreticalAmountMonthlyTest(remainingAmount)
    mn = min(pred,pred2)
    return min(1,self.presentInvestmentMonthly/mn)
  def gradeTotalJobLoss(self):
    # self.totalJobLoss
    if self.highLiquid > self.presentInvestmentValue:
      self.highLiquid = self.presentInvestmentValue
    if self.highLiquid >= self.totalJobLoss[0]:
      self.highLiquid = self.totalJobLoss[0]
      self.presentInvestmentValue -= self.highLiquid
    else:
      self.presentInvestmentValue -= self.highLiquid
    return min(self.highLiquid/self.totalJobLoss[0],1)
  def gradeHealthIns(self):
    # self.range_health =
    # self.job_loss =
    # self.retirementSave =
    # self.presentHealthInsuranceValue
    return min(1,self.presentHealthInsuranceValue/self.range_health[0])
  def gradeAll(self):
    # self.gradeHealth = self.gradeHealthIns()
    # self.gradeJobLoss = self.gradeTotalJobLoss()
    # self.gradeTotal = self.gradeTotalAmount()

    # allValue = sorted(allValue.items(),key = lambda x: x[1])
    self.order = ["Health","Job Loss","Total"]

    if self.gradeJobLoss - self.gradeTotal >= 0.2:
      if self.gradeHealth - self.gradeTotal >= 0.4:
        if self.gradeHealth - self.gradeJobLoss >= 0.2:
          self.order = self.order[::-1]
        else:
          self.order = ["Total","Health","Job Loss"]
      else:
        self.order = ["Health","Total","Job Loss"]
    else:
      if self.gradeHealth - self.gradeTotal >= 0.4:
        self.order = ["Job Loss","Total","Health"]
      else:
        if self.gradeHealth - self.gradeJobLoss >= 0.2:
          self.order = ["Job Loss","Health","Total"]
