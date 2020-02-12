from flask import Flask, render_template,request
from flask_sqlalchemy import SQLAlchemy
import requests
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





@app.route("/zomato")
def zomato(cuisine):
    print(cuisine)
    h={'user-key':'4febbc079d5c6e22700a69d421956a8d'}
    
    response=requests.get('https://developers.zomato.com/api/v2.1/cuisines?lat=28.697776&lon=77.1406&radius=4000',headers=h,params={'user-key':'4febbc079d5c6e22700a69d421956a8d'})
    r=response.json()
    for i in r['cuisines']:
        new1=i['cuisine']
        if new1['cuisine_name']==cuisine:





            response=requests.get('https://developers.zomato.com/api/v2.1/search?lat=28.697776&lon=77.1406&radius=4000&cuisines='+str(new1['cuisine_id']), headers=h,params={'user-key':'4febbc079d5c6e22700a69d421956a8d','sort':'rating','count':10})
            r=response.json()
            new=r['restaurants']
            return render_template('zomato.html',new=new)
    
    return render_template('index.html')



if __name__=="__main__":
    app.run()