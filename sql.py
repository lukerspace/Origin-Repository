import mysql.connector
import json
import os
from dotenv import load_dotenv
from getpass import getpass
from mysql.connector import pooling
from dotenv import load_dotenv
import os
import json
# 連結資料庫
## 啟動資料庫
load_dotenv()
# 只適用在booking sql


connection_pool = pooling.MySQLConnectionPool(
      host = os.getenv("SERVER_HOST"),
      # port = os.getenv("SERVER_PORT"),
      user = os.getenv("SERVER_USER"),
      password = os.getenv("SERVER_PASSWORD"),
      database = "taipei",
      charset = "utf8",
      auth_plugin='mysql_native_password'
   )


connection_object = connection_pool.get_connection()
if connection_object.is_connected():
   print("SQL is connected~~")
   connection_object.close()



# taipeiDB = init_db()
# taipeiCursor = taipeiDB.cursor()

# 關閉資料庫

def closePool(connection_object, taipeiCursor):
   if connection_object.is_connected():
      taipeiCursor.close()
      connection_object.close()


# conn = conn=mysql.connector.connect(host = "localhost",user=input("Enter username: "),password=getpass("Enter password: "), database = "taipei",charset = "utf8",auth_plugin='mysql_native_password')
conn = conn=mysql.connector.connect(host = os.getenv("SERVER_HOST"),user=os.getenv("SERVER_USER"),password=os.getenv("SERVER_PASSWORD"), database = "taipei",charset = "utf8",auth_plugin='mysql_native_password')
cursor = conn.cursor()
# attraction
def mysql_select(sql):
   conn=mysql.connector.connect(
      host = os.getenv("SERVER_HOST"),user=os.getenv("SERVER_USER"),
      password=os.getenv("SERVER_PASSWORD"), database = "taipei",
      charset = "utf8",auth_plugin='mysql_native_password'
      )
   cursor = conn.cursor()
   cursor.execute(sql)
   sql_result = cursor.fetchall()
   attraction_list = []
   for attration in sql_result:
      temp_attr = dict(zip(cursor.column_names, attration))
      temp_attr['images'] = json.loads(attration[9])
      attraction_list.append(temp_attr)
   cursor.close()   
   return attraction_list


# user
def user_select(**kargs):
   conn=mysql.connector.connect(
      host = os.getenv("SERVER_HOST"),user=os.getenv("SERVER_USER"),
      password=os.getenv("SERVER_PASSWORD"),database = "taipei",
      charset = "utf8",auth_plugin='mysql_native_password'
    )
   cursor = conn.cursor()
   sql=f'select * from user where '
   for i in kargs:
      sql+=f'{i} = \'{kargs[i]}\' and '
   sql=sql[:-5]
    # print(sql)
   cursor.execute(sql)
   user=cursor.fetchone()
   if user:
        userdata=(dict(zip(cursor.column_names,user)))
        print(userdata)
        cursor.close()
        return userdata
   else:
        return None

def user_insert(**kargs):
   conn=mysql.connector.connect(
      host = os.getenv("SERVER_HOST"),user=os.getenv("SERVER_USER"),
      password=os.getenv("SERVER_PASSWORD"),database = "taipei",
      charset = "utf8",auth_plugin='mysql_native_password'
   )
   cursor = conn.cursor()
   sql=f'insert into user '
   column = '('
   value = '('
   for i in kargs:
        column += i + ','
        value += f"\'{kargs[i]}\',"
   column = column[:-1] + ')'
   value = value[:-1] + ')'
   sql += column + ' VALUES ' + value
   # print(sql)
   cursor.execute(sql)
   conn.commit()
   cursor.close()
   
# 
# ====================
# for /api/booking
def selectBooking(**kwargs):
   try:
      connection_pool = pooling.MySQLConnectionPool(
      host = os.getenv("SERVER_HOST"),
      # port = os.getenv("SERVER_PORT"),
      user = os.getenv("SERVER_USER"),
      password = os.getenv("SERVER_PASSWORD"),
      database = "taipei",
      charset = "utf8",
      auth_plugin='mysql_native_password'
      )
   except Exception as e:
      print(e)  
   try:
      sql_cmd = f"""
               SELECT a.id, a.name, a.address, a.images, b.date, b.time, b.price  
               FROM booking b 
               JOIN attraction a ON b.attractionId = a.id 
               WHERE b.userId = { kwargs["userId"] }
               """

      connection_object = connection_pool.get_connection()

      if connection_object.is_connected():
         # print("connect_ok，連接有效")
         taipeiCursor = connection_object.cursor()
         taipeiCursor.execute(sql_cmd)               
         taipeiResult = taipeiCursor.fetchone()
         # print(taipeiResult,"訂單資料")
      if taipeiResult:
         bookingData = dict(zip(taipeiCursor.column_names, taipeiResult))

         # print(bookingData,"字典狀況")
         return bookingData
      else:
         return None
   except Exception as e:
      print(e)
      return None
   finally:
      closePool(connection_object, taipeiCursor)        

def insertBooking(**kwargs):
   try:
      connection_pool = pooling.MySQLConnectionPool(
      host = os.getenv("SERVER_HOST"),
      # port = os.getenv("SERVER_PORT"),
      user = os.getenv("SERVER_USER"),
      password = os.getenv("SERVER_PASSWORD"),
      database = "taipei",
      charset = "utf8",
      auth_plugin='mysql_native_password'
      )
   except Exception as e:
      print(e)  
   try:
      insertColumn = ''
      insertValue = ''
      for key in kwargs:
         insertColumn += f"{ key }, "
         if type(kwargs[key]) == str:
            insertValue += f"'{ kwargs[key] }', "
         else: 
            insertValue += f"{ kwargs[key] }, "

      insertColumn = insertColumn[:-2]
      insertValue = insertValue[:-2]

      sql_cmd = f"""
            INSERT INTO booking({ insertColumn })
            VALUES ({ insertValue })
            """

      connection_object = connection_pool.get_connection()

      if connection_object.is_connected():
         taipeiCursor = connection_object.cursor()
         taipeiCursor.execute(sql_cmd)      

         
                   
         connection_object.commit()
   except Exception as e:
      print(e)
   finally:
      closePool(connection_object, taipeiCursor)        

def updateBooking(userId, **kwargs):
   try:
      connection_pool = pooling.MySQLConnectionPool(
      host = os.getenv("SERVER_HOST"),
      # port = os.getenv("SERVER_PORT"),
      user = os.getenv("SERVER_USER"),
      password = os.getenv("SERVER_PASSWORD"),
      database = "taipei",
      charset = "utf8",
      auth_plugin='mysql_native_password'
      )
   except Exception as e:
      print(e)  
   try:
      updateColumnAndValue = ""

      for key in kwargs:
         if type(kwargs[key]) == str:
            updateColumnAndValue += f"{ key } = '{ kwargs[key] }', "
         else: 
            updateColumnAndValue += f"{ key } = { kwargs[key] }, "

      updateColumnAndValue = updateColumnAndValue[:-2]

      sql_cmd = f"""
            UPDATE booking 
            SET { updateColumnAndValue }
            WHERE userId = { userId }
            """

      connection_object = connection_pool.get_connection()

      if connection_object.is_connected():
         taipeiCursor = connection_object.cursor()
         taipeiCursor.execute(sql_cmd)                
         connection_object.commit()            
   except Exception as e:
      print(e)
   finally:
      closePool(connection_object, taipeiCursor)        

def deleteBookingData(**kwargs):
   try:
      connection_pool = pooling.MySQLConnectionPool(
      host = os.getenv("SERVER_HOST"),
      # port = os.getenv("SERVER_PORT"),
      user = os.getenv("SERVER_USER"),
      password = os.getenv("SERVER_PASSWORD"),
      database = "taipei",
      charset = "utf8",
      auth_plugin='mysql_native_password'
      )
   except Exception as e:
      print(e)  
   try:
      deleteId = kwargs["userId"]

      sql_cmd = f"""
            DELETE FROM booking
            WHERE userId = { deleteId }
            """

      connection_object = connection_pool.get_connection()

      if connection_object.is_connected():
         taipeiCursor = connection_object.cursor()
         taipeiCursor.execute(sql_cmd)                
         connection_object.commit()              
   except Exception as e:
      print(e)
   finally:
      closePool(connection_object, taipeiCursor)     


# API
# for /api/order
def insertOrder(**kwargs):
   try:
      connection_pool = pooling.MySQLConnectionPool(
         host = os.getenv("SERVER_HOST"),
         # port = os.getenv("SERVER_PORT"),
         user = os.getenv("SERVER_USER"),
         password = os.getenv("SERVER_PASSWORD"),
         database = "taipei",
         charset = "utf8",
         auth_plugin='mysql_native_password'
         )
   except Exception as e:
      print(e)  
   try:
      insertColumn = ''
      insertValue = ''

      for key in kwargs:
         insertColumn += f"{ key }, "
         if type(kwargs[key]) == str:
            insertValue += f"'{ kwargs[key] }', "
         else: 
            insertValue += f"{ kwargs[key] }, "

      insertColumn = insertColumn[:-2]
      insertValue = insertValue[:-2]

      sql_cmd = f"""
            INSERT INTO orders ({ insertColumn })
            VALUES ({ insertValue })
            """

      connection_object = connection_pool.get_connection()

      if connection_object.is_connected():
         taipeiCursor = connection_object.cursor()
         taipeiCursor.execute(sql_cmd)             
         connection_object.commit()
   except Exception as e:
      print(e)
   finally:
      closePool(connection_object, taipeiCursor)        

def selectOrder(number, userId):
   try:
      connection_pool = pooling.MySQLConnectionPool(
         host = os.getenv("SERVER_HOST"),
         # port = os.getenv("SERVER_PORT"),
         user = os.getenv("SERVER_USER"),
         password = os.getenv("SERVER_PASSWORD"),
         database = "taipei",
         charset = "utf8",
         auth_plugin='mysql_native_password'
         )
   except Exception as e:
      print(e)  
   try:
      sql_cmd = f"""
               SELECT 
                  o.number, o.price, o.date, o.time, o.status, o.attractionId, o.phone,
                  a.name AS attr_name, a.address, a.images,
                  u.name AS user_name, u.email
               FROM orders o
               JOIN attraction a ON o.attractionId = a.id
               JOIN user u ON o.userId = u.id
               WHERE o.number = '{ number }' AND o.userId = { userId }
               """

      connection_object = connection_pool.get_connection()

      if connection_object.is_connected():
         taipeiCursor = connection_object.cursor()
         taipeiCursor.execute(sql_cmd)                
         taipeiResult = taipeiCursor.fetchone()

      if taipeiResult:
         orderData = dict(zip(taipeiCursor.column_names, taipeiResult))
         return orderData
      else:
         return None
   except Exception as e:
      print(e)
      return None
   finally:
      closePool(connection_object, taipeiCursor) 

def updateOrder(number, **kwargs):
   try:
      connection_pool = pooling.MySQLConnectionPool(
         host = os.getenv("SERVER_HOST"),
         # port = os.getenv("SERVER_PORT"),
         user = os.getenv("SERVER_USER"),
         password = os.getenv("SERVER_PASSWORD"),
         database = "taipei",
         charset = "utf8",
         auth_plugin='mysql_native_password'
         )
   except Exception as e:
      print(e)  

   try:
      updateColumnAndValue = ""

      for key in kwargs:
         if type(kwargs[key]) == str:
            updateColumnAndValue += f"{ key } = '{ kwargs[key] }', "
         else: 
            updateColumnAndValue += f"{ key } = { kwargs[key] }, "

      updateColumnAndValue = updateColumnAndValue[:-2]

      sql_cmd = f"""
            UPDATE orders 
            SET { updateColumnAndValue }
            WHERE number = '{ number }'
            """

      connection_object = connection_pool.get_connection()

      if connection_object.is_connected():
         taipeiCursor = connection_object.cursor()
         taipeiCursor.execute(sql_cmd)                
         connection_object.commit()            
   except Exception as e:
      print(e)
   finally:
      closePool(connection_object, taipeiCursor)

def selectOrders(userId):
   try:
      connection_pool = pooling.MySQLConnectionPool(
         host = os.getenv("SERVER_HOST"),
         # port = os.getenv("SERVER_PORT"),
         user = os.getenv("SERVER_USER"),
         password = os.getenv("SERVER_PASSWORD"),
         database = "taipei",
         charset = "utf8",
         auth_plugin='mysql_native_password'
         )
   except Exception as e:
      print(e)  
   orderDataList = []
   try:
      sql_cmd = f"""
               SELECT o.number, o.attractionId, o.status, a.name AS attr_name
               FROM orders o
               JOIN attraction a ON o.attractionId = a.id
               WHERE o.userId = { userId }
               """

      connection_object = connection_pool.get_connection()

      if connection_object.is_connected():
         taipeiCursor = connection_object.cursor()
         taipeiCursor.execute(sql_cmd)                
         taipeiResults = taipeiCursor.fetchall()

      if taipeiResults:
         for taipeiResult in taipeiResults:
            orderData = dict(zip(taipeiCursor.column_names, taipeiResult))
            orderDataList.append(orderData)
         return orderDataList
      else:
         return None
   except Exception as e:
      print(e)
      return None
   finally:
      closePool(connection_object, taipeiCursor)


def insertOrder(**kwargs):
   try:
      connection_pool = pooling.MySQLConnectionPool(
         host = os.getenv("SERVER_HOST"),
         # port = os.getenv("SERVER_PORT"),
         user = os.getenv("SERVER_USER"),
         password = os.getenv("SERVER_PASSWORD"),
         database = "taipei",
         charset = "utf8",
         auth_plugin='mysql_native_password'
         )
   except Exception as e:
      print(e)  
   try:
      insertColumn = ''
      insertValue = ''

      for key in kwargs:
         insertColumn += f"{ key }, "
         if type(kwargs[key]) == str:
            insertValue += f"'{ kwargs[key] }', "
         else: 
            insertValue += f"{ kwargs[key] }, "

      insertColumn = insertColumn[:-2]
      insertValue = insertValue[:-2]

      sql_cmd = f"""
            INSERT INTO orders ({ insertColumn })
            VALUES ({ insertValue })
            """

      connection_object = connection_pool.get_connection()

      if connection_object.is_connected():
         taipeiCursor = connection_object.cursor()
         taipeiCursor.execute(sql_cmd)             
         connection_object.commit()
   except Exception as e:
      print(e)
   finally:
      closePool(connection_object, taipeiCursor)        

def selectOrder(number, userId):
   try:
      connection_pool = pooling.MySQLConnectionPool(
         host = os.getenv("SERVER_HOST"),
         # port = os.getenv("SERVER_PORT"),
         user = os.getenv("SERVER_USER"),
         password = os.getenv("SERVER_PASSWORD"),
         database = "taipei",
         charset = "utf8",
         auth_plugin='mysql_native_password'
         )
   except Exception as e:
      print(e)     
   try:
      sql_cmd = f"""
               SELECT 
                  o.number, o.price, o.date, o.time, o.status, o.attractionId, o.phone,
                  a.name AS attr_name, a.address, a.images,
                  u.name AS user_name, u.email
               FROM orders o
               JOIN attraction a ON o.attractionId = a.id
               JOIN user u ON o.userId = u.id
               WHERE o.number = '{ number }' AND o.userId = { userId }
               """

      connection_object = connection_pool.get_connection()

      if connection_object.is_connected():
         taipeiCursor = connection_object.cursor()
         taipeiCursor.execute(sql_cmd)                
         taipeiResult = taipeiCursor.fetchone()

      if taipeiResult:
         orderData = dict(zip(taipeiCursor.column_names, taipeiResult))
         return orderData
      else:
         return None
   except Exception as e:
      print(e)
      return None
   finally:
      closePool(connection_object, taipeiCursor) 

def updateOrder(number, **kwargs):
   try:
      connection_pool = pooling.MySQLConnectionPool(
         host = os.getenv("SERVER_HOST"),
         # port = os.getenv("SERVER_PORT"),
         user = os.getenv("SERVER_USER"),
         password = os.getenv("SERVER_PASSWORD"),
         database = "taipei",
         charset = "utf8",
         auth_plugin='mysql_native_password'
         )
   except Exception as e:
      print(e)  
   try:
      updateColumnAndValue = ""

      for key in kwargs:
         if type(kwargs[key]) == str:
            updateColumnAndValue += f"{ key } = '{ kwargs[key] }', "
         else: 
            updateColumnAndValue += f"{ key } = { kwargs[key] }, "

      updateColumnAndValue = updateColumnAndValue[:-2]

      sql_cmd = f"""
            UPDATE orders 
            SET { updateColumnAndValue }
            WHERE number = '{ number }'
            """

      connection_object = connection_pool.get_connection()

      if connection_object.is_connected():
         taipeiCursor = connection_object.cursor()
         taipeiCursor.execute(sql_cmd)                
         connection_object.commit()            
   except Exception as e:
      print(e)
   finally:
      closePool(connection_object, taipeiCursor)

def selectOrders(userId):
   try:
      connection_pool = pooling.MySQLConnectionPool(
         host = os.getenv("SERVER_HOST"),
         # port = os.getenv("SERVER_PORT"),
         user = os.getenv("SERVER_USER"),
         password = os.getenv("SERVER_PASSWORD"),
         database = "taipei",
         charset = "utf8",
         auth_plugin='mysql_native_password'
         )
   except Exception as e:
      print(e)  
   orderDataList = []
   try:
      sql_cmd = f"""
               SELECT o.number, o.attractionId, o.status, a.name AS attr_name
               FROM orders o
               JOIN attraction a ON o.attractionId = a.id
               WHERE o.userId = { userId }
               """

      connection_object = connection_pool.get_connection()

      if connection_object.is_connected():
         taipeiCursor = connection_object.cursor()
         taipeiCursor.execute(sql_cmd)                
         taipeiResults = taipeiCursor.fetchall()

      if taipeiResults:
         for taipeiResult in taipeiResults:
            orderData = dict(zip(taipeiCursor.column_names, taipeiResult))
            orderDataList.append(orderData)
         return orderDataList
      else:
         return None
   except Exception as e:
      print(e)
      return None
   finally:
      closePool(connection_object, taipeiCursor)