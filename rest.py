import numpy as np 
import pandas as pd 
import re

data = pd.read_csv('zomato.csv', encoding ='latin1')
country = pd.read_excel("Country-Code.xlsx")
data1 = pd.merge(data, country, on='Country Code')

abels = list(data1.Country.value_counts().index)
values = list(data1.Country.value_counts().values)

res_India = data1[data1.Country == 'India']
labels1 = list(res_India.City.value_counts().index)
values1 = list(res_India.City.value_counts().values)
labels1 = labels1[:10]
values1 = values1[:10]

NCR = ['New Delhi','Gurgaon','Noida','Faridabad']
res_NCR = res_India[(res_India.City == NCR[0])|(res_India.City == NCR[1])|(res_India.City == NCR[2])|
                    (res_India.City == NCR[3])]
agg_rat = res_NCR[res_NCR['Aggregate rating'] > 0]




NCR = ['New Delhi','Gurgaon','Noida','Faridabad']
res_NCR = res_India[(res_India.City == NCR[0])|(res_India.City == NCR[1])|(res_India.City == NCR[2])|
                    (res_India.City == NCR[3])]
agg_rat = res_NCR[res_NCR['Aggregate rating'] > 0]


res_India['Cuisines'].value_counts().sort_values(ascending=False).head(10)


res_India = data1[data1.Country == 'India']
NCR = ['New Delhi','Gurgaon','Noida','Faridabad']
res_NCR = res_India[(res_India.City == NCR[0])|(res_India.City == NCR[1])|(res_India.City == NCR[2])|
                    (res_India.City == NCR[3])]

data_new_delphi=res_NCR[['Restaurant Name','Cuisines','Locality','Aggregate rating', 'Votes']]
C = data_new_delphi['Aggregate rating'].mean()
print(C)
#2.39583438526

m = data_new_delphi['Votes'].quantile(0.90)
print(m)
#234.0

# Filter out all qualified restaurants into a new DataFrame
q_restaurant = data_new_delphi.copy().loc[data_new_delphi['Votes'] >= m]
q_restaurant.shape
#(795, 5)

# Function that computes the weighted rating of each restaurant
def weighted_rating(x, m=m, C=C):
    v = x['Votes']
    R = x['Aggregate rating']
    # Calculating the score
    return (v/(v+m) * R) + (m/(m+v) * C)
# Define a new feature 'score' and calculate its value with `weighted_rating()`
q_restaurant['score'] = q_restaurant.apply(weighted_rating, axis=1)

#Sort restaurant based on score calculated above
q_restaurant = q_restaurant.sort_values('score', ascending=False)
#Print the top 10 restaurants in Delhi NCR
q_restaurant[['Restaurant Name','Cuisines', 'Locality','Votes', 'Aggregate rating', 'score']].head(10)

print(q_restaurant)
