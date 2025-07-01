from pandas.core.frame import DataFrame
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn import preprocessing

data: DataFrame = pd.read_csv("SecondHand_Cars_dataset_2025-06-25.csv")

print(data.head())

pd.get_dummies(data, drop_first=True)

corr = data.corr(numeric_only=True)
fig, ax = plt.subplots()
fig.set_size_inches(9, 7)
print("plotting")
sns.heatmap(corr, annot=True, fmt='.1f', cmap='RdBu', center=0, ax=ax)