import functions as func
import pandas as pd
import matplotlib as mpl
import numpy as np

df = pd.read_csv(r"C:\Users\SymbiotyK\Desktop\gitHub\Python-projects\DataFrameManipulation\Analyzing Sales Data\vgsales.csv")

platforms = func.remove_dups(df,"Platform")
dateofrel = func.remove_dups(df,"Year")

SalesSum = df.groupby(["Platform"])[df.columns[-5:]].sum()
SalesSum = SalesSum.sort_values(by="Global_Sales",ascending=False)
SalesSum = SalesSum.eval()
print(SalesSum.head())