import pandas as pd
import numpy as np
df = pd.read_csv('G:/flask website/placement.csv')

x = df.iloc[:,0:1].values
y = df.iloc[:,1].values


from sklearn.linear_model import LinearRegression

lr = LinearRegression()
lr.fit(x,y)
import pickle

pickle.dump(lr,open('model.pkl','wb'))
