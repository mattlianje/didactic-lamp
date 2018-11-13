import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from apyori import apriori

ta_data = pd.read_csv("apriori_title.csv", header=None)
print(ta_data.head())
records = []
for i in range(0, 6272):
    records.append([str(ta_data.values[i,j]) for j in range(0, 42)])

association_rules = apriori(records, min_support=0.00159, min_confidence=0.1, min_lift=0.5, min_length=2)
association_results = list(association_rules)

print(association_results)
#print(len(association_rules))
#print(association_rules[0])
