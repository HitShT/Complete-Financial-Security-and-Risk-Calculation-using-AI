import pandas as pd
from sklearn import linear_model
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from statistics import stdev

df = pd.read_csv("Complete_AI_Prediction_DS.csv")

df = df[df.investment != 0]

'''
    Cols to drop
    "investment",
    "year_start_investing",
    "health_insurance",
    "health_emergency",
    "investment_stopped",
    "job_loss",
    "remaining_investment_return",
    "investment_return",
    "health_emergency_amount",
    "months_out_job",
    "total_spent_job_loss",
    "total_returns_before_withdrawl",
    "amount_taken",
    "health_emergency_amount",
    "investment_stopped_year"


    Remaining Columns
    "salary"
    "monthly_expense"
    "dependents"
    "investment_amount_monthly"
    "health_insurance_amount"
    "total_amount_end"
'''

years = []
for i in range(2000):
    if df["investment"][i]:
        years.append(2021-df["year_start_investing"][i])
    else:
        years.append(0)

cols = [
    "investment",
    "year_start_investing",
    "health_insurance",
    "health_emergency",
    "investment_stopped",
    "job_loss",
    "remaining_investment_return",
    "investment_return",
    "health_emergency_amount",
    "months_out_job",
    "total_spent_job_loss",
    "total_returns_before_withdrawl",
    "amount_taken",
    "health_emergency_amount",
    "investment_stopped_year"
]

df = df.drop(columns = cols)

df["years_invested"] = years

def display():
    plt.scatter(list(df["salary"]),list(df["total_amount_end"]),color = "red")
    plt.title('Salary Vs Total Savings', fontsize=14)
    plt.xlabel("Average Salary (adjusted for inflation)")
    plt.ylabel("Total Savings")
    plt.grid(True)
    plt.show()

    plt.scatter(list(df["monthly_expense"]),list(df["total_amount_end"]),color = "red")
    plt.title('Monthly Expense Vs Total Savings', fontsize=14)
    plt.xlabel("Monthly Expense (adjusted for inflation)")
    plt.ylabel("Total Savings")
    plt.grid(True)
    plt.show()

    plt.scatter(list(df["dependents"]),list(df["total_amount_end"]),color = "red")
    plt.title('Dependents Vs Total Savings', fontsize=14)
    plt.xlabel("Dependents")
    plt.ylabel("Total Savings")
    plt.grid(True)
    plt.show()

    plt.scatter(list(df["investment_amount_monthly"]),list(df["total_amount_end"]),color = "red")
    plt.title('Monthly Investment Amount Vs Total Savings', fontsize=14)
    plt.xlabel("Monthly Investment Amount (Adjusted for inflation)")
    plt.ylabel("Total Savings")
    plt.grid(True)
    plt.show()

accuracy = {
    "Multiple Linear Regression" : [],
    "Polynomial Regression" : [],
    "Lasso Regression" : [],
    "Ridge Regression" : []
}

def getAccuracy(y,pred,model):
    average = 0
    y = list(y)
    for i in range(len(y)):
        average += (abs(y[i]-pred[i])/pred[i])*100
    accuracy[model].append(average/len(y))


def getAccuracyPlot(y,y_pred,model):
    plt.scatter(y,y_pred,color = "red")
    plt.title('Actual Vs Predicted using {}'.format(model), fontsize=14)
    plt.xlabel("Actual Value")
    plt.ylabel("Predicted Value")
    plt.grid(True)
    plt.show()

# display()
health_insurance_amount = []
for i in range(2000):
    health_insurance_amount.append(df["health_insurance_amount"][i]*100000)

# df["health_insurance_amount"] = health_insurance_amount

X = df[[
    "salary",
    "monthly_expense",
    "dependents",
    "total_amount_end",
    "health_insurance_amount",
    "years_invested"
]]

y = df["investment_amount_monthly"]

def getModelAccuracy(accuracy):
    for i in accuracy:
        print("Mean",sum(accuracy[i])/len(accuracy[i]))
        print("Standard deviation",stdev(accuracy[i]))
def multipleLinReg():
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)
    regr = linear_model.LinearRegression()
    regr.fit(X_train, y_train)
    pred = regr.predict(X_test)
    getAccuracy(y_test,pred,"Multiple Linear Regression")
    # getAccuracyPlot(y_test,pred,"Multi Linear Regression")

def polynomialReg():
    poly = PolynomialFeatures(degree = 5)
    poly_variables = poly.fit_transform(X)
    regr = linear_model.LinearRegression()
    X_train, X_test, y_train, y_test = train_test_split(poly_variables, y, test_size=0.33)
    regr.fit(X_train,y_train)
    pred = regr.predict(X_test)
    getAccuracy(y_test,pred,"Polynomial Regression")
    # getAccuracyPlot(y_test,pred,"Polynomial Regression")

def lassoModel():
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)
    regr = linear_model.Lasso()
    regr.fit(X_train,y_train)
    pred = regr.predict(X_test)
    getAccuracy(y_test,pred,"Lasso Regression")
    # getAccuracyPlot(y_test,pred,"Lasso Model")

def ridgeModel():
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)
    regr = linear_model.Ridge()
    regr.fit(X_train,y_train)
    pred = regr.predict(X_test)
    getAccuracy(y_test,pred,"Ridge Regression")
    # getAccuracyPlot(y_test,pred,"Ridge Model")

for i in range(1000):
    multipleLinReg()
    polynomialReg()
    lassoModel()
    ridgeModel()

# accuracy_df = pd.DataFrame(accuracy)
# accuracy_df.to_csv("accuracy_check1.csv",sep=',',index=False)


getModelAccuracy(accuracy)

accuracy = {
    "Multiple Linear Regression" : [],
    "Polynomial Regression" : [],
    "Lasso Regression" : [],
    "Ridge Regression" : []
}

df["health_insurance_amount"] = health_insurance_amount

for i in range(1000):
    multipleLinReg()
    polynomialReg()
    lassoModel()
    ridgeModel()

getModelAccuracy(accuracy)
