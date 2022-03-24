from email.mime.text import MIMEText
import smtplib
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
 
def send_email(email, height, average_h, amt_of_people):
    from_email = 'ataime365@gmail.com'
    gmail_password = os.getenv('GMAIL_PASSWORD')
    from_password = gmail_password #Genarate App password
    to_email = email #passed to the function from the app.py

    subject = "Height data"
    message = f"Hey there, your height is <strong>{height} cm</strong>. <br> The Average height is <strong>{average_h}</strong> cm, calculated over <strong>{amt_of_people}</strong> people" #This line is just a text

    msg = MIMEText(message, 'html') #This converts that text from message to html enabled #This is a MIMEText oj=bject, object of the class
    msg['Subject'] = subject
    msg['To'] = to_email
    msg['From'] = from_email

    #To login to my gmail
    gmail = smtplib.SMTP('smtp.gmail.com', 587) #587 is the port, smtp.gmail.com is the server
    gmail.ehlo()
    gmail.starttls()
    gmail.login(from_email, from_password)
    gmail.send_message(msg)