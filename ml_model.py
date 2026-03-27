# Bird Species Observation Analysis Project
# Author: Sarthak Mishra
# Description: Data Cleaning, Analysis, Visualization, and DashboardS
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

df = pd.read_csv('data/cleaned_dataset.csv').dropna(subset=['Common_Name'])

le = LabelEncoder()
df['label'] = le.fit_transform(df['Common_Name'])

X = df[['Temperature','Humidity','Month']].fillna(0)
y = df['label']

X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2)

model = RandomForestClassifier()
model.fit(X_train,y_train)

print("Accuracy:", model.score(X_test,y_test))
