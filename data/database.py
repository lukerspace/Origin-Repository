import mysql.connector
import os
import json
from getpass import getpass


conn=mysql.connector.connect(host = "localhost",user=input("Enter username: "),password=getpass("Enter password: "),\
     database = "taipei",charset = "utf8",auth_plugin='mysql_native_password')
cursor=conn.cursor()

with open("taipei-attractions.json", "r", encoding="utf-8") as f:
   data_obj = json.load(f)
   data = data_obj["result"]["results"]

   for item in data:
      id = item["_id"]
      name = item["stitle"]
      category = item["CAT2"]
      description = item["xbody"]
      address = item["address"]
      transport = item["info"]
      mrt = item["MRT"]
      latitude = float(item["latitude"])
      longitude = float(item["longitude"])
      multi_url = item["file"].split("http://")[1:]
      urlList = []
      for url in multi_url:
         if url.endswith(("jpg", "JPG", "png", "PNG")):
            url = "http://" + url
            urlList.append(url)
            
      # print(urlList)
      urlJson=json.dumps(urlList)
      # print(urlJson)

      sql="""
         INSERT INTO attraction (id, name, category, description, address, transport, mrt, latitude, longitude, images)
         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
         """

      cursor.execute(sql,(id, name, category, description, address, transport, mrt, latitude, longitude, urlJson))
      conn.commit()
   



# print("當前路徑 -> %s" %os.getcwd())
