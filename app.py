import os
from flask import Flask,render_template, request, url_for,redirect
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.sql import func #import sqlalchemy functions
import pymysql


app=Flask(__name__)#create the flask app object with the name of the current module

#Database Configuration with MySQL --> db type | username: password | path to database name    
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:''@localhost/learnsqlalchemy'
db=SQLAlchemy(app)#create the database object

class UserInfo(db.Model):
    #create a column in the database table
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(100),unique=True)
    password=db.Column(db.String(100))

    def __init__(self, username, password): #constructor of the UserInfo class
      self.username = username
      self.password = password

# admin1=UserInfo('admin1','password1')
# '''create the database table based on the python model 
#     -> e.g. there's UserInfo and BookMetadata classes,
#     then there will be two tables in the database'''
# db.session.add(admin1) #add the admin1 object to the database
# db.session.commit() #commit the changes to the database
# UserInfo.query.all() #query to show all the data in the UserInfo table

@app.route('/')
def index():
    return render_template('index.html')

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

if __name__=='__main__':
    app.run()