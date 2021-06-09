from flask import *
from getpass import getpass
from config import Config
# import os
# import json
# import mysql.connector 

from api.attraction_api import appAttraction 
from api.user_api import appUser
from api.book_api import appBooking
from api.order_api import api_order

app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.config["JSON_SORT_KEYS"] = False
app.secret_key="hello"


app.register_blueprint(appAttraction, url_prefix='/api')
app.register_blueprint(appUser, url_prefix='/api')
app.register_blueprint(appBooking, url_prefix='/api')
app.register_blueprint(api_order, url_prefix="/api")

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

# app.run(port=3000)
# 
app.run(host="0.0.0.0",port=3000)

