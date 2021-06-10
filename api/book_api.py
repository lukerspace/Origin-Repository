import sys
sys.path.append("..")

from flask import request, Blueprint, jsonify, session
from datetime import datetime
import json

from sql import selectBooking, insertBooking, updateBooking, deleteBookingData, user_insert
 
appBooking = Blueprint("appBooking", __name__) 

@appBooking.route("/booking", methods=["GET"])
def getBooking():
   try:
      if "user" in session:
         userId = int(session["user"]["id"])
         # print(userId,"is in the session")
         selectedBooking = selectBooking(userId = userId)
         # print(selectedBooking,"資料填入")
         if selectedBooking:
            data = {
               "attraction": {
                  "id": selectedBooking["id"],
                  "name": selectedBooking["name"],
                  "address": selectedBooking["address"],
                  "image": json.loads(selectedBooking["images"])[0]
               },
               "date": datetime.strftime(selectedBooking["date"], "%Y-%m-%d"),
               "time": selectedBooking["time"],
               "price": selectedBooking["price"],
            }
            print("客戶:",session["user"]["name"],"有訂單")
            return jsonify({ "data": data })
         else:
            print("客戶:",session["user"]["name"],"沒有訂單")
            return jsonify({ "data": None })
      else:
         print("尚未登入")
         return jsonify({ "error": True, "message": "請先登入" })            
   except Exception as e:
      print(e)
      return jsonify({ "error": True, "message": "伺服器內部錯誤" })
      
@appBooking.route("/booking", methods=["POST"])
def postBooking(): 
   try:
      if "user" in session:
         # print("成功記入POST方法")
         attractionId = int(request.get_json()["attractionId"])
         date = request.get_json()["date"]
         time = request.get_json()["time"]
         price = int(request.get_json()["price"])
         userId = int(session["user"]["id"])
   #       #  紀錄4
         
         # print(attractionId,date,time,userId,price,"POST資料寫入")
          
         if not (attractionId and date and time and price and userId):
            print("資料存在錯誤")
            return jsonify({ "error": True, "message": "建立失敗，輸入不正確或其他原因" })
         
         originBooking = selectBooking(userId = userId)
         print(originBooking,"原本訂單")

         if originBooking:
            updateBooking(userId, attractionId = attractionId, date = date, time = time, price = price)
         else:
         # if originBooking:
            insertBooking(attractionId = attractionId, date = date, time = time, price = price, userId = userId)
         
         return jsonify({ "ok": True })
      else:
         return jsonify({ "error": True, "message": "請先登入" })
   except Exception as e:
      print(e)
      return jsonify({ "error": True, "message": "伺服器內部錯誤" })




@appBooking.route("/booking", methods=["DELETE"])
def deleteBooking():
   try:
      if "user" in session:
         userId = request.get_json()["userId"]
         deleteBookingData(userId = userId)

         deletedBooking = selectBooking(userId = userId)
         if not deletedBooking:
            return jsonify({ "ok": True })
         else:
            return jsonify({ "error": True, "message": "刪除失敗" })
      else:
         return jsonify({ "error": True, "message": "未登入系統，拒絕存取" })
   except Exception as e:
      print(e)
      return jsonify({ "error": True, "message": "伺服器內部錯誤" })