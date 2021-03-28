import pandas as pd

def clean(file):
    df = pd.read_csv(file)
    typeFund = list(df["Type"])
    for i in range(len(typeFund)):
        tmp = list(set(typeFund[i].split("//")))
        tmp = ",".join(tmp)
        typeFund[i] = str(tmp)
    df["Type"] = typeFund
    df.to_csv(file,sep=',',index=False)

files = [
    "mfBondDetails.csv",
    "mfEquityDetails.csv"
]

for i in files:
    clean(i)
