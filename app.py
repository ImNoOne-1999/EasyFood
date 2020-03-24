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
    
        
        #swiggy scrap data
        
        headers = {
                'authority': 'www.swiggy.com','__fetch_req__': 'true','user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36','content-type': 'application/json',
                'accept': '*/*','sec-fetch-site': 'same-origin','sec-fetch-mode': 'cors','referer': 'https://www.swiggy.com/nagpur?page=2','accept-encoding': 'gzip, deflate, br','accept-language': 'en-US,en;q=0.9',
                'cookie': '__SW=HoKO60a2TJk5HNQSliXxoCrZ5HWyjz2D; _device_id=0894e1e8-2d2b-4895-9d14-d612cabd8650; _gcl_aw=GCL.1579978783.EAIaIQobChMImru0zref5wIVGg4rCh0rPQtzEAAYASAAEgJTR_D_BwE; _gcl_au=1.1.537344729.1579978783; _ga=GA1.2.965912730.1579978783; _gac_0=1.1579978783.EAIaIQobChMImru0zref5wIVGg4rCh0rPQtzEAAYASAAEgJTR_D_BwE; optimizelyEndUserId=lo_BOlBS0CG5G4W; order_source=Google-Sok; order_medium=CPC; order_campaign=google_search_sok_food_na_narm_order_web_m_web_clubbedcities_v3_welcome50_neev_competitor_newuser_competitor_bmm; __cfduid=d717f5774b2b57fe77139c34294ac76211582631293; fontsLoaded=1; userLocation=%7B%22lat%22%3A%2221.11021%22%2C%22lng%22%3A%2279.047786%22%2C%22address%22%3A%22Deendayal%20Nagar%2C%20Nagpur%2C%20Maharashtra%20440022%2C%20India%22%2C%22area%22%3A%22Deendayal%20Nagar%22%2C%22id%22%3A%2233379943%22%7D; _gid=GA1.2.1343453737.1582728551; _parsely_session={%22sid%22:2%2C%22surl%22:%22https://bytes.swiggy.com/swiggy-rest-opinionated-crud-library-on-spring-a78715074eb4%22%2C%22sref%22:%22https://www.google.com/%22%2C%22sts%22:1582728550837%2C%22slts%22:1580357610757}; _parsely_visitor={%22id%22:%22pid=d60e514ce147de51e436db833c907f56%22%2C%22session_count%22:2%2C%22last_session_ts%22:1582728550837}; _guest_tid=28fd9621-459a-4e16-9a2d-6daf8f88adba; _sid=lbw58cea-759d-47df-89df-b6ebbc1e349d; _gat_UA-53591212-4=1',
        }

        params = (
                ('page', 1),('ignoreServiceability', 'true'),('lat', lat),('lng', lon),('str', cuisine),('pageType', 'SEE_ALL'),('sortBy', 'RELEVANCE'),('page_type', 'DESKTOP_SEE_ALL_LISTING'),('count',5)
        )
 
        response = requests.get('https://www.swiggy.com/dapi/restaurants/list/v5', headers=headers, params=params)
        response = response.text
        data1 = json.loads(response)
        data1 = data1['data']['cards']

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
                response=requests.get('https://developers.zomato.com/api/v2.1/search?lat='+lat+'&lon='+lon+'&radius=4000&cuisines='+str(new1['cuisine_id']), headers=h,params={'user-key':'4febbc079d5c6e22700a69d421956a8d','sort':'rating','count':5})
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
            response=requests.get('https://developers.zomato.com/api/v2.1/search?lat='+lat+'&lon='+lon+'&radius=4000&cuisines='+str(new1['cuisine_id']), headers=h,params={'user-key':'4febbc079d5c6e22700a69d421956a8d','sort':'rating','count':5})
            r=response.json()
            new=r['restaurants']
            return render_template('temp.html',new=new,newg = newg)
        

    return render_template('index.html')
    
@app.route("/swiggy11")
def swiggy():
    item = 'noodles'

    headers = {
    'authority': 'www.swiggy.com',
    'sec-fetch-dest': 'empty',
    '__fetch_req__': 'true',
    'usecache': 'false',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
    'content-type': 'application/json',
    'accept': '*/*',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'referer': 'https://www.swiggy.com/search?q=milkshake',
    'accept-language': 'en-US,en;q=0.9',
    'cookie': '__SW=HoKO60a2TJk5HNQSliXxoCrZ5HWyjz2D; _device_id=0894e1e8-2d2b-4895-9d14-d612cabd8650; _gcl_aw=GCL.1579978783.EAIaIQobChMImru0zref5wIVGg4rCh0rPQtzEAAYASAAEgJTR_D_BwE; _gcl_au=1.1.537344729.1579978783; _ga=GA1.2.965912730.1579978783; _gac_0=1.1579978783.EAIaIQobChMImru0zref5wIVGg4rCh0rPQtzEAAYASAAEgJTR_D_BwE; optimizelyEndUserId=lo_BOlBS0CG5G4W; __cfduid=d717f5774b2b57fe77139c34294ac76211582631293; fontsLoaded=1; _parsely_visitor=^{^%^22id^%^22:^%^22pid=d60e514ce147de51e436db833c907f56^%^22^%^2C^%^22session_count^%^22:6^%^2C^%^22last_session_ts^%^22:1584731511829^}; _guest_tid=c22cd0fb-0ee9-4785-b9c3-158641fefd49; _sid=ltqe5fe6-e1e3-4b4b-a3cd-f6d15b71bc98; _gid=GA1.2.589395445.1585041707; userLocation=^{^%^22address^%^22:^%^22Pune^%^2C^%^20Maharashtra^%^2C^%^20India^%^22^%^2C^%^22area^%^22:^%^22^%^22^%^2C^%^22deliveryLocation^%^22:^%^22Pune^%^22^%^2C^%^22lat^%^22:18.5204303^%^2C^%^22lng^%^22:73.8567437^}; dadl=true; _gat_0=1; _gat_UA-53591212-4=1',
    }

    params = (
    ('lat', '18.5204303^'),
    ('lng', '73.8567437^'),
    ('trackingId', '593ed602-00e6-999a-8abd-e58a23308a11^'),
    ('str', 'milkshake^'),
    ('sld', 'false^'),
    ('non_partner_search', 'false^'),
    ('submitAction', 'ENTER'),
    )

    response = requests.get('https://www.swiggy.com/dapi/restaurants/search/v2_2', headers=headers, params=params)
    response = response.text
    data1 = json.loads(response)
    print(data1)
    data1 = data1['data']['cards']
    
    return render_template('swig.html',data1=data1)


if __name__=="__main__":
    app.run()