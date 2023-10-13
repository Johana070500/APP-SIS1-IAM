from flask import Flask,  render_template, request, redirect, url_for, session 
from flask_mysqldb import MySQL,MySQLdb 
from os import path 
from notifypy import Notify

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'app_iam'
mysql = MySQL(app)

@app.route('/')
def home():
    return render_template("contenido.html")    


if __name__=='__main__':
    app.run(debug=True)