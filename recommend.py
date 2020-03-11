import pandas as pd
from scipy import sparse
from sklearn.metrics.pairwise import cosine_similarity

restaurants = pd.read_csv('nagpur1.csv')
restaurants.head()



user_ratings = restaurants.pivot_table(index=['id'],columns=['name'],values='avgRating')
user_ratings.head()
print(user_ratings)