
import pandas as pd
from models import Accomodation


df = pd.read_csv("accomodation_final.csv")
df_cols = df.columns


for i in range(len(df)):
    data = {}
    query = ""
    for col in df_cols:
        data[col] = df.loc[i][col]
    query = query + col + "=" + df.loc[i][col]
    Accomodation.objects.create()
print("finish")