import pandas as pd
import requests
from bs4 import BeautifulSoup


df = pd.read_csv("corporateBonds.csv")
linksCorporate = df["Links"]

result = {} #name : 1y 3y 5y SIP

for i in linksCorporate:
    try:
        page = requests.get("http://"+i)
        soup = BeautifulSoup(page.content, 'lxml')

        name = soup.find_all("div", {"class": "fund-info-content withImg"})
        name = name[0].find("h1")
        name = name.findAll(text = True)[0]

        entryCost =soup.find_all("table", {"class": "key-parameters-details key-parameters-table"})
        entryCost = entryCost[0].find_all("td",{'class':"item","colspan":"2"})
        entryCost = entryCost[0].findAll(text = True)[-1]
        entryCost = entryCost.split("&")[0]
        entryCost = entryCost.split()[1]
        entryCost = int(entryCost[1:])

        results = soup.find_all("div", {"class": "grey-theme-table"})
        results = results[0].find("tbody")
        results = results.find("tr")
        results = results.find_all("td")
        ans = []
        for i in range(len(results)):
            ans.append(results[i].findAll(text = True)[0])
        ans = ans[:-1]
        while len(ans) < 3:
            ans.append("-")
        ans.append(entryCost)
        result[name] = ans
    except Exception as e:
        continue

name = [i for i in result]
y1 = []
y3 = []
y5 = []
amt = []
for i in result:
    y1.append(result[i][0])
    y3.append(result[i][1])
    y5.append(result[i][2])
    amt.append(result[i][3])

name.append("HDFC Savings")
y1.append(3)
y3.append(3)
y5.append(3)
amt.append(0)

name.append("SBI Savings")
y1.append(2.7)
y3.append(2.7)
y5.append(2.7)
amt.append(0)

name.append("ICICI Savings")
y1.append(3)
y3.append(3)
y5.append(3)
amt.append(0)

name.append("Kotak Savings")
y1.append(3.5)
y3.append(3.5)
y5.append(3.5)
amt.append(0)

name.append("Axis Savings")
y1.append(3)
y3.append(3)
y5.append(3)
amt.append(0)

name.append("IndusInd Savings")
y1.append(4)
y3.append(4)
y5.append(4)
amt.append(0)

name.append("Yes Bank Savings")
y1.append(3)
y3.append(3)
y5.append(3)
amt.append(0)

name.append("PNB Savings")
y1.append(3)
y3.append(3)
y5.append(3)
amt.append(0)

name.append("BoB Savings")
y1.append(3)
y3.append(3)
y5.append(3)
amt.append(0)

name.append("BoI Savings")
y1.append(2.9)
y3.append(2.9)
y5.append(2.9)
amt.append(0)

name.append("HDFC FD")
y1.append(4.9)
y3.append(5.15)
y5.append(5.3)
amt.append(5000)

name.append("SBI FD")
y1.append(4.9)
y3.append(5.3)
y5.append(5.4)
amt.append(1000)

name.append("ICICI FD")
y1.append(4.9)
y3.append(5.35)
y5.append(5.5)
amt.append(10000)

name.append("Kotak FD")
y1.append(4.5)
y3.append(5.1)
y5.append(5.3)
amt.append(5000)

name.append("Axis FD")
y1.append(5.15)
y3.append(5.4)
y5.append(5.75)
amt.append(10000)

name.append("IndusInd FD")
y1.append(6.5)
y3.append(7.36)
y5.append(7.61)
amt.append(10000)

name.append("Yes Bank FD")
y1.append(5.83)
y3.append(6.92)
y5.append(6.92)
amt.append(10000)

name.append("PNB FD")
y1.append(5.3)
y3.append(5.7)
y5.append(6.02)
amt.append(10000)

name.append("BoB FD")
y1.append(5)
y3.append(5.25)
y5.append(5.25)
amt.append(1000)

name.append("BoI FD")
y1.append(5.25)
y3.append(5.3)
y5.append(5.3)
amt.append(10000)


df = {
    "Name" :name,
    "Return after 1 Year":y1,
    "Return after 3 Year":y3,
    "Return after 5 Year":y5,
    "Minimum SIP Amount":amt
}

df = pd.DataFrame(df)
df.to_csv("corporateBondsDetails.csv",sep=',',index=False)
