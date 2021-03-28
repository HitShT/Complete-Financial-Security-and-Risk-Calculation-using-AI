from requests import get
from bs4 import BeautifulSoup
import pandas

# url = "https://www.moneycontrol.com/mutual-funds/performance-tracker/returns/large-cap-fund.html"
url = [
"https://www.moneycontrol.com/mutual-funds/performance-tracker/returns/large-cap-fund.html",
"https://www.moneycontrol.com/mutual-funds/performance-tracker/returns/multi-cap-fund.html",
"https://www.moneycontrol.com/mutual-funds/performance-tracker/returns/large-and-mid-cap-fund.html",
"https://www.moneycontrol.com/mutual-funds/performance-tracker/returns/mid-cap-fund.html",
"https://www.moneycontrol.com/mutual-funds/performance-tracker/returns/small-cap-fund.html",
"https://www.moneycontrol.com/mutual-funds/performance-tracker/returns/value-fund.html",
"https://www.moneycontrol.com/mutual-funds/performance-tracker/returns/contra-fund.html",
"https://www.moneycontrol.com/mutual-funds/performance-tracker/returns/focused-fund.html",
"https://www.moneycontrol.com/mutual-funds/performance-tracker/returns/sectoral/thematic.html",
"https://www.moneycontrol.com/mutual-funds/performance-tracker/returns/long-duration-fund.html",
"https://www.moneycontrol.com/mutual-funds/performance-tracker/returns/medium-to-long-duration-fund.html",
"https://www.moneycontrol.com/mutual-funds/performance-tracker/returns/medium-duration-fund.html",
"https://www.moneycontrol.com/mutual-funds/performance-tracker/returns/dynamic-bond-fund.html",
"https://www.moneycontrol.com/mutual-funds/performance-tracker/returns/short-duration-fund.html",
"https://www.moneycontrol.com/mutual-funds/performance-tracker/returns/low-duration-fund.html",
"https://www.moneycontrol.com/mutual-funds/performance-tracker/returns/ultra-short-duration-fund.html",
"https://www.moneycontrol.com/mutual-funds/performance-tracker/returns/liquid-fund.html"
]

fund_type = [
    "Large Cap",
    "Multi Cap",
    "Large and Mid Cap",
    "Mid Cap",
    "Small Cap",
    "Value",
    "Contra",
    "Focused",
    "Thematic",
    "Long Duration",
    "Medium to Long Duration",
    "Medium Duration",
    "Dynamic Bond",
    "Short Duration",
    "Low Duration",
    "Ultra short duration",
    "Liquid"
]

# st = set()
link_mf = []
type = []

def getPortfolioLink(url,type_fund):
    response = get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    funds_table = soup.find(id = "dataTableId")
    row = funds_table.find_all("a",href=True)
    funds_links = []
    for i in row:
        funds_links.append(i["href"])
    # global st
    for i in funds_links:
        try:
            url = i
            response = get(url)
            soup = BeautifulSoup(response.text, 'lxml')
            link = soup.find_all("a",attrs = {
                "title":"Detailed Portfolio Analysis"
            },href=True)
            if "portfolio-overview" in link[0]["href"] or "portfolio-debt" in link[0]["href"]:
                link_mf.append(link[0]["href"])
                type.append(type_fund)
                # st.add(link[0]["href"])
        except:
            continue

ct = 1
for i in range(len(url)):
    print("Start",ct)
    getPortfolioLink(url[i],fund_type[i])
    print("Done",ct) #Status count
    ct += 1

# data = list(st)
# df = pandas.DataFrame(data,columns = ["Link"])
# df.to_csv("mutualFundLinks.csv",sep=',',index=False)

print(link_mf,type)

df = {
    "Link" : link_mf,
    "Type" : type
}

df = pandas.DataFrame(df)
df.to_csv("mutualFundLinks.csv",sep=',',index=False)
