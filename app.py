from flask import Flask, render_template,request
from flask_sqlalchemy import SQLAlchemy
import requests
import json
import sys
import numpy as np 
import pandas as pd 
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from nltk.tokenize import word_tokenize
sys.stdout.reconfigure(encoding='utf-8')

from flask import request, redirect, url_for
from flask_security import Security, SQLAlchemyUserDatastore,UserMixin,RoleMixin,login_required
# from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:sri@localhost/flaskbeg'
app.config['SECRET_KEY'] = 'super-secret'
app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_PASSWORD_HASH'] = "plaintext"

app.debug = True
db = SQLAlchemy(app)



roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)



@app.route("/")
@app.route("/index",methods=['POST','GET'])
def index():
    if request.method == 'POST':

        data_temp = recommend1()
        #dish zomato medd krna hai abhi
        cuisine = request.form['name']

        city_name = request.form['city']
        print(city_name)
        city_name = city_name.split(' ')
        city_name = '%20'.join(city_name)
        h={'user-key':'07adec2c50dd0fe4adee163b0fe1b35a'}
        response = requests.get('https://developers.zomato.com/api/v2.1/locations?query='+city_name,headers=h,params={'user-key':'07adec2c50dd0fe4adee163b0fe1b35a'})
        r=response.json()

        lat = str(r['location_suggestions'][0]['latitude'])
        lon = str(r['location_suggestions'][0]['longitude'])


        h={'user-key':'4febbc079d5c6e22700a69d421956a8d'}
        response=requests.get('https://developers.zomato.com/api/v2.1/cuisines?lat='+lat+'&lon='+lon+'&radius=4000',headers=h,params={'user-key':'4febbc079d5c6e22700a69d421956a8d'})
        r=response.json()
    
        
        #swiggy scrap data dynamic done for dishes
        
        headers = {
                'authority': 'www.swiggy.com','sec-fetch-dest': 'empty','__fetch_req__': 'true',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
            }

        params = (
                ('lat', lat),('lng', lon),('trackingId', 'bb2d4d4f-c6c6-6c70-1364-d99132620a33'),('str', cuisine),('sld', 'false'),
                ('non_partner_search', 'false'),('submitAction', 'ENTER'),
            )

        response = requests.get('https://www.swiggy.com/dapi/restaurants/search/v2_2', headers=headers, params=params)
        data1 = response.json()
        data1 = data1['data']['restaurants']

        #restaurants info passing
        for i in r['cuisines']:
            new1=i['cuisine']
            #print(new1)
            #print(cuisine)
            if new1['cuisine_name'].lower()==cuisine.lower():
                #near by restaurants
                response=requests.get('https://developers.zomato.com/api/v2.1/geocode?lat='+lat+'&lon='+lon+'&radius=4000',headers=h,params={'user-key':'4febbc079d5c6e22700a69d421956a8d','count':5})
                r1=response.json()
                newg = r1['nearby_restaurants']

                #top rated restaurants
                response=requests.get('https://developers.zomato.com/api/v2.1/search?lat='+lat+'&lon='+lon+'&radius=4000&cuisines='+str(new1['cuisine_id']), headers=h,params={'user-key':'4febbc079d5c6e22700a69d421956a8d','sort':'relevance','count':10})
                r=response.json()
                new=r['restaurants']
                return render_template('zomato.html',new=new,data1=data1,newg=newg,data_temp=data_temp)
        return render_template('index.html')   
    else:
        return render_template('index.html')

    
        


@app.route("/profile/<email>")
@login_required
def profile(email):
    user = User.query.filter_by(email=email).first()
    return render_template('profile.html',user = user)


@app.route("/post_user", methods=['POST'])
def post_user():
    user = User(request.form['username'],request.form['email'])
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('index'))



def recommend1():
    #load the dataset
    data = pd.read_csv('zomato.csv', encoding ='latin1')

    data['City'].value_counts(dropna = False)

    data_city =data.loc[data['City'] == 'New Delhi']    
    data_new_delphi=data_city[['Restaurant Name','Cuisines','Locality','Aggregate rating']]
    data_new_delphi['Locality'].value_counts(dropna = False).head(5)
    data_new_delphi.loc[data['Locality'] == 'Connaught Place']


    data_sample=[]
    def restaurant_recommend_func(location,title):   
        global data_sample       
        global cosine_sim
        global sim_scores
        global tfidf_matrix
        global corpus_index
        global feature
        global rest_indices
        global idx

        
        # When location comes from function ,our new data consist only location dataset
        data_sample = data_new_delphi.loc[data_new_delphi['Locality'] == location]  
        
        # index will be reset for cosine similarty index because Cosine similarty index has to be same value with result of tf-idf vectorize
        data_sample.reset_index(level=0, inplace=True) 
        
        #Feature Extraction
        data_sample['Split']="X"
        for i in range(0,data_sample.index[-1]):
            split_data=re.split(r'[,]', data_sample['Cuisines'][i])
            for k,l in enumerate(split_data):
                split_data[k]=(split_data[k].replace(" ", ""))
            split_data=' '.join(split_data[:])
            data_sample['Split'].iloc[i]=split_data
            
        #TF-IDF vectorizer
        #Extracting Stopword
        tfidf = TfidfVectorizer(stop_words='english')
        #Replace NaN for empty string
        data_sample['Split'] = data_sample['Split'].fillna('')
        #Applying TF-IDF Vectorizer
        tfidf_matrix = tfidf.fit_transform(data_sample['Split'])
        tfidf_matrix.shape
        
        # Using for see Cosine Similarty scores
        feature= tfidf.get_feature_names()
        #Cosine Similarity
        # Compute the cosine similarity matrix
        cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix) 
        
        # Column names are using for index
        corpus_index=[n for n in data_sample['Split']]
        
        #Construct a reverse map of indices    
        indices = pd.Series(data_sample.index, index=data_sample['Restaurant Name']).drop_duplicates() 
        
        #index of the restaurant matchs the cuisines
        idx = indices[title]
        #Aggregate rating added with cosine score in sim_score list.
        sim_scores=[]
        for i,j in enumerate(cosine_sim[idx]):
            k=data_sample['Aggregate rating'].iloc[i]
            if j != 0 :
                sim_scores.append((i,j,k))
                
        #Sort the restaurant names based on the similarity scores
        sim_scores = sorted(sim_scores, key=lambda x: (x[1],x[2]) , reverse=True)
        # 10 similar cuisines
        sim_scores = sim_scores[0:10]
        rest_indices = [i[0] for i in sim_scores] 
    
        data_x =data_sample[['Restaurant Name','Aggregate rating']].iloc[rest_indices]
        
        data_x['Cosine Similarity']=0
        for i,j in enumerate(sim_scores):
            data_x['Cosine Similarity'].iloc[i]=round(sim_scores[i][1],2)
    
        return data_x

    
    # Top 10 similar restaurant with cuisine of 'Pizza Hut' restaurant in Connaught Place
    data_temp = restaurant_recommend_func('Connaught Place','Pizza Hut')

    return data_temp


@app.route("/swiggy")
def zomato():

    cuisine = "BBQ"
    
    city_name = "new delhi"
    city_name = city_name.split(' ')
    city_name = '%20'.join(city_name)
    h={'user-key':'07adec2c50dd0fe4adee163b0fe1b35a'}
    response=requests.get('https://developers.zomato.com/api/v2.1/locations?query='+city_name,
                      headers=h,params={'user-key':'07adec2c50dd0fe4adee163b0fe1b35a'})
    r=response.json()

    lat = str(r['location_suggestions'][0]['latitude'])
    lon = str(r['location_suggestions'][0]['longitude'])

 
    h={'user-key':'4febbc079d5c6e22700a69d421956a8d'}
    response=requests.get('https://developers.zomato.com/api/v2.1/cuisines?lat='+lat+'&lon='+lon+'&radius=4000',headers=h,params={'user-key':'4febbc079d5c6e22700a69d421956a8d'})
    r=response.json()
        
    for i in r['cuisines']:
        new1=i['cuisine']
        #print(new1)
        #print(cuisine)
        if new1['cuisine_name']==cuisine:
            response=requests.get('https://developers.zomato.com/api/v2.1/geocode?lat='+lat+'&lon='+lon+'&radius=4000',headers=h,params={'user-key':'4febbc079d5c6e22700a69d421956a8d','count':5})
            r1=response.json()
            newg = r1['nearby_restaurants']
            response=requests.get('https://developers.zomato.com/api/v2.1/search?lat='+lat+'&lon='+lon+'&radius=4000&cuisines='+str(new1['cuisine_id']), headers=h,params={'user-key':'4febbc079d5c6e22700a69d421956a8d','sort':'rating','count':10})
            r=response.json()
            new=r['restaurants']
            return render_template('temp.html',new=new,newg = newg)
        

    return render_template('index.html')
    



if __name__=="__main__":
    app.run()