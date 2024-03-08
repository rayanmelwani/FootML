import pandas as pd
import numpy as np
from numpy.random import default_rng
import csv
import unidecode

points_dict = {}
df = pd.read_csv("justpoints.csv")

for row in df.itertuples():
    points_dict[row.name] = row.pred_points

df2 = pd.read_csv("database/cleaned_simple_database_21_22.csv")
for line, row in df2.iterrows():
    for name in points_dict:
        df2.loc[df2.Name == name, "pred_points"] = points_dict[name]

print(points_dict['Willian Borges Da Silva'])
print(df2)

df2.drop(['Unnamed: 0'], axis=1, inplace=True)

df2.to_csv("database/cleaned_simple_database_21_22.csv")
