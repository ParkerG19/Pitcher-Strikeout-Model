import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import model_selection
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split


col_to_extract_1 = ["Name", "GS", "SO9","SO"]
df = pd.read_csv("player_standard_pitching.csv", usecols=col_to_extract_1)
print(df.corr())


col_to_extract_2 = []
