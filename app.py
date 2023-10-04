import os
from flask import Flask,render_template, request, url_for,redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import create_database, database_exists

from sqlalchemy.sql import func #import sqlalchemy functions
from sqlalchemy import update,create_engine,select #import sqlalchemy update function and create_engine function
from sqlalchemy.orm import sessionmaker #import sqlalchemy session maker function
import pymysql

app=Flask(__name__)#create the flask app object with the name of the current module

engine_url='mysql+pymysql://root:''@localhost/learnsqlalchemy'
# if not database_exists(engine_url):
#     create_database(engine_url)
# #Database Configuration with MySQL --> db type | username: password | path to database name    
app.config['SQLALCHEMY_DATABASE_URI']=engine_url

engine=create_engine(engine_url)
Session=sessionmaker(engine)

db=SQLAlchemy(app)#create the database object

class UserInfo(db.Model):
    #create a column in the database table
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(100),unique=True)
    password=db.Column(db.String(100))

    def __init__(self, username, password): #constructor of the UserInfo class
      self.username = username
      self.password = password

@app.route('/')
def index():
    data = UserInfo.query.all() #get all the data from the UserInfo table
    search_query = 'hadehtiga'
    
    search_statement = select(UserInfo).where(UserInfo.username == search_query)
    with Session() as session:
        result = session.query(UserInfo).filter_by(username=search_query).first()
        username = result.username if result else None # get the username from the search result
        print(username)
    return render_template('index.html', data=data, search_result=username)

#create button function
@app.route('/add_user', methods=['POST'])
def add_user():
    db.create_all() #create the database table based on the python model
    if request.method=='POST':
         username=request.form['username'] #get the username data from the form
         password=request.form['password'] #get the password data from the form
 
         new_user=UserInfo(username,password) #create a new user object
 
         db.session.add(new_user) #add the new user object to the database
         db.session.commit()
 
         return redirect(url_for('index'))
    
@app.route('/update_user', methods=['POST'])
def update_user():
    if request.method=='POST':
        new_username=request.form['n_username']
        old_username=request.form['o_username']
        update_statement=(update(UserInfo)
                            .where(UserInfo.username==old_username)
                            .values(username=new_username)
                            .execution_options(synchronize_session=False))
        with Session() as session:
            session.execute(update_statement)
            session.commit()
        return redirect(url_for('index'))
    

if __name__=='__main__':
    app.run()