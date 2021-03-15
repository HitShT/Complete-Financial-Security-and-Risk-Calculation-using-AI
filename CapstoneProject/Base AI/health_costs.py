import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from matplotlib import pyplot as plt
df = pd.read_csv("Per Capita Health Expenditure.csv")
df = df.dropna()
df = df.drop(columns=['Amount( in USD)', 'USD to INR'])

# for i in df:
#     print(i)
# print(df["Amount in INR"])
model = ARIMA(df["Amount in INR"],order=(2,1,1))
result = model.fit()
yhat = list(result.predict(19,39,typ="levels")) #19 to 39 means 1999 to 1979
# print(help(result.predict))
# print(result.summary())
# print(yhat)
# year = {2000-1-i:yhat[i] for i in range(len(yhat))}
# print(df)
for i in range(len(yhat)):
    temp = {
        "Year":[2000-i-1],
        "Amount in INR":[yhat[i]]
    }
    temp = pd.DataFrame(data = temp)
    df = df.append(temp)
df.to_csv("temp.csv",sep=',',index=False)
