from flask import Flask, render_template,request
from flask_sqlalchemy import SQLAlchemy
import requests
import json
import sys
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
        
        cuisine = request.form['name']
        

        h={'user-key':'4febbc079d5c6e22700a69d421956a8d'}
    
        response=requests.get('https://developers.zomato.com/api/v2.1/cuisines?lat=28.697776&lon=77.1406&radius=4000',headers=h,params={'user-key':'4febbc079d5c6e22700a69d421956a8d'})
        r=response.json()


        for i in r['cuisines']:
            new1=i['cuisine']
            print(new1)
            print(cuisine)
            if new1['cuisine_name']==cuisine:
                response=requests.get('https://developers.zomato.com/api/v2.1/search?lat=21.1458&lon=79.0882&radius=4000&cuisines='+str(new1['cuisine_id']), headers=h,params={'user-key':'4febbc079d5c6e22700a69d421956a8d','sort':'rating','count':10})
                r=response.json()
                new=r['restaurants']
                return render_template('zomato.html',new=new)
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





@app.route("/swiggy")
def zomato():

    
    headers = {
        'authority': 'www.swiggy.com',
        '__fetch_req__': 'true',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
        'content-type': 'application/json',
        'accept': '*/*',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'referer': 'https://www.swiggy.com/nagpur?page=2',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'cookie': '__SW=HoKO60a2TJk5HNQSliXxoCrZ5HWyjz2D; _device_id=0894e1e8-2d2b-4895-9d14-d612cabd8650; _gcl_aw=GCL.1579978783.EAIaIQobChMImru0zref5wIVGg4rCh0rPQtzEAAYASAAEgJTR_D_BwE; _gcl_au=1.1.537344729.1579978783; _ga=GA1.2.965912730.1579978783; _gac_0=1.1579978783.EAIaIQobChMImru0zref5wIVGg4rCh0rPQtzEAAYASAAEgJTR_D_BwE; optimizelyEndUserId=lo_BOlBS0CG5G4W; order_source=Google-Sok; order_medium=CPC; order_campaign=google_search_sok_food_na_narm_order_web_m_web_clubbedcities_v3_welcome50_neev_competitor_newuser_competitor_bmm; __cfduid=d717f5774b2b57fe77139c34294ac76211582631293; fontsLoaded=1; userLocation=%7B%22lat%22%3A%2221.11021%22%2C%22lng%22%3A%2279.047786%22%2C%22address%22%3A%22Deendayal%20Nagar%2C%20Nagpur%2C%20Maharashtra%20440022%2C%20India%22%2C%22area%22%3A%22Deendayal%20Nagar%22%2C%22id%22%3A%2233379943%22%7D; _gid=GA1.2.1343453737.1582728551; _parsely_session={%22sid%22:2%2C%22surl%22:%22https://bytes.swiggy.com/swiggy-rest-opinionated-crud-library-on-spring-a78715074eb4%22%2C%22sref%22:%22https://www.google.com/%22%2C%22sts%22:1582728550837%2C%22slts%22:1580357610757}; _parsely_visitor={%22id%22:%22pid=d60e514ce147de51e436db833c907f56%22%2C%22session_count%22:2%2C%22last_session_ts%22:1582728550837}; _guest_tid=28fd9621-459a-4e16-9a2d-6daf8f88adba; _sid=lbw58cea-759d-47df-89df-b6ebbc1e349d; _gat_UA-53591212-4=1',
    }

    params = (
        ('page', '0'),
        ('ignoreServiceability', 'true'),
        ('lat', '21.145800'),
        ('lng', ' 79.088158'),
        ('pageType', 'SEE_ALL'),
        ('sortBy', 'RELEVANCE'),
        ('page_type', 'DESKTOP_SEE_ALL_LISTING'),
    )

    response = requests.get('https://www.swiggy.com/dapi/restaurants/list/v5', headers=headers, params=params)
    response = response.text
    data = json.loads(response)
    page_nos = data['data']['pages']

    pag = 0
    for i in range(page_nos):
        headers = {
            'authority': 'www.swiggy.com',
            '__fetch_req__': 'true',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
            'content-type': 'application/json',
            'accept': '*/*',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'referer': 'https://www.swiggy.com/nagpur?page=2',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'cookie': '__SW=HoKO60a2TJk5HNQSliXxoCrZ5HWyjz2D; _device_id=0894e1e8-2d2b-4895-9d14-d612cabd8650; _gcl_aw=GCL.1579978783.EAIaIQobChMImru0zref5wIVGg4rCh0rPQtzEAAYASAAEgJTR_D_BwE; _gcl_au=1.1.537344729.1579978783; _ga=GA1.2.965912730.1579978783; _gac_0=1.1579978783.EAIaIQobChMImru0zref5wIVGg4rCh0rPQtzEAAYASAAEgJTR_D_BwE; optimizelyEndUserId=lo_BOlBS0CG5G4W; order_source=Google-Sok; order_medium=CPC; order_campaign=google_search_sok_food_na_narm_order_web_m_web_clubbedcities_v3_welcome50_neev_competitor_newuser_competitor_bmm; __cfduid=d717f5774b2b57fe77139c34294ac76211582631293; fontsLoaded=1; userLocation=%7B%22lat%22%3A%2221.11021%22%2C%22lng%22%3A%2279.047786%22%2C%22address%22%3A%22Deendayal%20Nagar%2C%20Nagpur%2C%20Maharashtra%20440022%2C%20India%22%2C%22area%22%3A%22Deendayal%20Nagar%22%2C%22id%22%3A%2233379943%22%7D; _gid=GA1.2.1343453737.1582728551; _parsely_session={%22sid%22:2%2C%22surl%22:%22https://bytes.swiggy.com/swiggy-rest-opinionated-crud-library-on-spring-a78715074eb4%22%2C%22sref%22:%22https://www.google.com/%22%2C%22sts%22:1582728550837%2C%22slts%22:1580357610757}; _parsely_visitor={%22id%22:%22pid=d60e514ce147de51e436db833c907f56%22%2C%22session_count%22:2%2C%22last_session_ts%22:1582728550837}; _guest_tid=28fd9621-459a-4e16-9a2d-6daf8f88adba; _sid=lbw58cea-759d-47df-89df-b6ebbc1e349d; _gat_UA-53591212-4=1',
        }

        params = (
            ('page', pag),
            ('ignoreServiceability', 'true'),
            ('lat', '21.145800'),
            ('lng', ' 79.088158'),
            ('pageType', 'SEE_ALL'),
            ('sortBy', 'RELEVANCE'),
            ('page_type', 'DESKTOP_SEE_ALL_LISTING'),
        )

        response = requests.get('https://www.swiggy.com/dapi/restaurants/list/v5', headers=headers, params=params)
        response = response.text
        pag += 1
        print("page no is "+ str(pag))
        data1 = json.loads(response)
        data1 = data1['data']['cards']
        
            

    return render_template('temp.html',data1=data1)
    



if __name__=="__main__":
    app.run()