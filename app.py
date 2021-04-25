from flask import *
import json
import mysql.connector 
from flask import *
from sql import cursor, conn , mysql_select
from getpass import getpass
# from config import Config

app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.config["JSON_SORT_KEYS"] = False

conn=mysql.connector.connect(
		host = "localhost",
		user=input("Enter username: "),
		password=getpass("Enter password: "),
		database = "taipei",charset = "utf8",
		auth_plugin='mysql_native_password')
cursor=conn.cursor()

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


@app.route('/api/attractions')
def attractions():
	if request.args.get('page'):
		page = request.args.get('page')
		page=int(page)
		index = page * 12
		next_page_JSON = page + 1
		if request.args.get('keyword'):
			keyword =request.args.get('keyword')
			attraction_JSON = mysql_select(f"SELECT * FROM attraction WHERE name LIKE '%{keyword}%' LIMIT {index},12")
			next_list= mysql_select(f"SELECT * FROM attraction WHERE name LIKE '%{keyword}%' LIMIT {index + 12}, 12")
			if len(next_list) == 0:
				next_page_JSON = None
			data = {"nextPage": next_page_JSON,"data": attraction_JSON}
			return jsonify(data)
		else:
			attraction_JSON = mysql_select(f"SELECT * FROM attraction LIMIT {index}, 12")
			next_list = mysql_select(f"SELECT * FROM attraction LIMIT {index + 12}, 12")
			print("目前頁面:",page)
			if index+1<320:
				print("起始ID:",index+1)
			if len(next_list) == 0:
				next_page_JSON = None
			data = {"nextPage": next_page_JSON,"data": attraction_JSON}
			return jsonify(data)
	return {"error": True,"message": "伺服器內部錯誤"}, 500

@app.route('/api/attraction/<int:ID>')
def api_attraction(ID):
	if ID:
		cursor.execute(f"SELECT * FROM attraction where id={ID}")
		data = cursor.fetchone()
		if data:
			attraction = {"data": dict(zip(cursor.column_names, data))}
			attraction['data']['images'] = json.loads(data[9])
			return attraction
		return jsonify({ "error": True, "message": "景點編號不正確" })
	
	return jsonify({ "error": True, "message": "伺服器內部錯誤" })


app.run(host="0.0.0.0",port=3000)



