import requests
from bs4 import BeautifulSoup
url = "https://www.etmoney.com/mutual-funds/debt/corporate-bond/61"
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
results = soup.find_all("h3", {"class": "scheme-name"})
links = []
for i in range(len(results)):
    results[i] = results[i].find_all('a', href=True)
    for j in results[i]:
        links.append("www.etmoney.com"+j["href"])

import pandas as pd

df = {
    "Links" : links
}

df = pd.DataFrame(df)
df.to_csv("corporateBonds.csv",sep=',',index=False)
