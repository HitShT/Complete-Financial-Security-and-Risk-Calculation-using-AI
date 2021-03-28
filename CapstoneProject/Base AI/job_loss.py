import pandas as pd
from sklearn import linear_model
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from statistics import stdev
df = pd.read_csv("Complete_AI_Prediction_DS.csv")


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
    "total_returns_before_withdrawl",
    "amount_taken",
    "health_emergency_amount",
    "investment_stopped_year",
    "health_insurance_amount",
    "total_amount_end",


    Remaining Columns
    "salary",
    "monthly_expense",
    "dependents",
    "investment_amount_monthly",
    "total_spent_job_loss",
'''

def getAccuracy(y,pred,model):
    average = 0
    y = list(y)
    for i in range(len(y)):
        average += (abs(y[i]-pred[i])/abs(pred[i]))*100
    accuracy[model].append(average/len(y))

def getAccuracyPlot(y,y_pred,model):
    plt.scatter(y,y_pred,color = "red")
    plt.title('Actual Vs Predicted using {}'.format(model), fontsize=14)
    plt.xlabel("Actual Value")
    plt.ylabel("Predicted Value")
    plt.grid(True)
    plt.show()

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

total_spent_job_loss = list(df["total_spent_job_loss"])
monthly_expense = list(df["monthly_expense"])
for i in range(2000):
    total_spent_job_loss[i] += 3*monthly_expense[i]

df["total_spent_job_loss"] = total_spent_job_loss

df = df[df.job_loss != 0]

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
    "total_returns_before_withdrawl",
    "amount_taken",
    "health_emergency_amount",
    "investment_stopped_year",
    "health_insurance_amount",
    "total_amount_end",
]

df = df.drop(columns = cols)

accuracy = {
    "Multiple Linear Regression" : [],
    "Polynomial Regression" : [],
    "Lasso Regression" : [],
    "Ridge Regression" : []
}

X = df[[
    "salary",
    "monthly_expense",
    "dependents",
    "investment_amount_monthly",
]]

y = df['total_spent_job_loss']

for i in range(1000):
    multipleLinReg()
    polynomialReg()
    lassoModel()
    ridgeModel()

getModelAccuracy(accuracy)
