# Bird Species Observation Analysis Project
# Author: Sarthak Mishra
# Description: Data Cleaning, Analysis, Visualization, and Dashboard
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('data/cleaned_dataset.csv')

print("Total Records:", len(df))
print("Unique Species:", df['Scientific_Name'].nunique())

# Species diversity
df.groupby('Habitat')['Scientific_Name'].nunique().plot(kind='bar')
plt.title("Species Diversity by Habitat")
plt.show()

# Monthly trend
df.groupby('Month').size().plot()
plt.title("Monthly Trend")
plt.show()

# Top species
df['Common_Name'].value_counts().head(10).plot(kind='bar')
plt.title("Top 10 Species")
plt.show()
