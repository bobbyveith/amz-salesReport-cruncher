import pandas as pd

#Ingest AMZ Report CSV & convert to dataframe
AMAZON_REPORT = "./Amazon Report.csv"

df = pd.read_csv(AMAZON_REPORT)
print(df.head)

#Transfrom Data