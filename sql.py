import mysql.connector
import json
from getpass import getpass

# conn = conn=mysql.connector.connect(host = "localhost",user=input("Enter username: "),password=getpass("Enter password: "), database = "taipei",charset = "utf8",auth_plugin='mysql_native_password')
conn = conn=mysql.connector.connect(host = "localhost",user="root",password="0000", database = "taipei",charset = "utf8",auth_plugin='mysql_native_password')

cursor = conn.cursor()

def mysql_select(sql):
	cursor.execute(sql)
	sql_result = cursor.fetchall()
	attraction_list = []
	for attration in sql_result:
		temp_attr = dict(zip(cursor.column_names, attration))
		temp_attr['images'] = json.loads(attration[9])
		attraction_list.append(temp_attr)
	
	return attraction_list

   
