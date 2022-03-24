import os
from dotenv import load_dotenv, find_dotenv
from flask import Flask, render_template, request 
from flask_sqlalchemy import SQLAlchemy #inside the init method of flask_sqlalchemy
from send_email import send_email
from sqlalchemy.sql import func

load_dotenv(find_dotenv())
db_password = os.getenv('POSTGRE_PASSWORD')

app = Flask(__name__) #instanciating an object or a Flask object
app.config['SQLALCHEMY_DATABASE_URI']=f'postgresql://postgres:{db_password}@localhost/height_collector' #username:password@localhost/database_name
db = SQLAlchemy(app) #we are creating an SQLAlchemy object for our app (flask app)

#creating the class blueprint #Setting rules
class Data(db.Model): #inheriting from the model class of SQLAlchemy
    #SQL Rules for creating the table
    __tablename__ = 'data'
    id = db.Column(db.Integer, primary_key=True) #Id is the primary key, as usual #Already autoincremental by default
    #class variables
    email_d = db.Column(db.String(120), unique=True) #String not more than 120 characters
    height_d = db.Column(db.Integer)

    #Lets initialize the variables of our object
    def __init__(self, email_d, height_d):
        self.email_d = email_d
        self.height_d = height_d


@app.route('/') # @ decorator, '/' link to the home page or main page
def index_page():
    return render_template("index.html")


@app.route('/success', methods=['POST']) # because of the POST method in the form in the html
def success_page(): #success_page is the link for html
    if request.method == 'POST':
        #catching the data sent from the index page
        email = request.form["email_name"] #print(request.form) to see the full data coming from the form
        height = request.form['height_name'] #This gets the data from the frontend to the backend #POST request
        print(email, height)
        
        # print(db.session.query(Data).filter(Data.email_d == email).count()) #SELECT data.id AS data_id, data.email_d AS data_email_d, data.height_d AS data_height_d FROM data WHERE data.email_d = %(email_d_1)s
        if db.session.query(Data).filter(Data.email_d == email).count() == 0:
            #creating an instance of our Data class
            data1 = Data(email, height) #def __init__(self, email_d, height_d):
            db.session.add(data1) #To add the rows to the database object
            db.session.commit()
            #Get the average after you have commited new changes
            average_height = db.session.query(func.avg(Data.height_d)).scalar()
            average_height = round(average_height, 1) #To round up
            amount_of_people = db.session.query(Data.email_d).count()
            send_email(email, height, average_height, amount_of_people)
            return render_template("success.html")
            #Adding the text to the index.html page using the safe method
        else:
            average_height = db.session.query(func.avg(Data.height_d)).scalar()
            average_height = round(average_height, 1)
            amount_of_people = db.session.query(Data.email_d).count()
            send_email(email, height, average_height, amount_of_people)
            return render_template("index.html", text="Seems like we've got something from that email address already")
    return render_template("index.html", text="Seems like we've got something from that email address already") #This acts like an else statement for both if statements

if __name__ == "__main__":
    app.debug = True
    app.run()
