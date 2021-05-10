# from config import Config
from flask import *
import json
import mysql.connector 
from sql import cursor, conn , mysql_select
from getpass import getpass
from config import Config
from api.attraction_api import attraction_api


app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.config["JSON_SORT_KEYS"] = False

app.register_blueprint(attraction_api, url_prefix='/api')

# Pages
@app.route("/")
def index():
	return render_template("index.html")
@app.route("/attraction/<id>")
def attraction(id):
	return render_template("attraction.html")
@app.route("/booking")
def booking():
	return render_template("booking.html")
@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")



app.run(port=3000)
# app.run(host="0.0.0.0",port=3000)



