import sys
sys.path.append("..")

from flask import request, Blueprint, jsonify, session
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import os
import json
import requests

from sql import insertOrder, selectOrder, updateOrder, selectOrders
 
load_dotenv()

api_order = Blueprint("api_order", __name__)

@api_order.route("/orders", methods=["POST"])
def postOrders():
   try:
      if "user" in session:
         # Set Main Keys to Variables
         requestJson = request.get_json()
         # print(requestJson)
         orderJson = requestJson["order"]
         tripJson = orderJson["trip"]
         attractionJson = tripJson["attraction"]
         contactJson = orderJson["contact"]

         # Get information
         prime = requestJson["prime"]

         price = int(orderJson["price"])

         attractionId = int(attractionJson["id"])
         attractionName = attractionJson["name"]
         attractionAddress = attractionJson["address"]
         attractionImage = attractionJson["image"]
         attractionBoolean = attractionId and attractionName and attractionAddress and attractionImage

         date = tripJson["date"]
         time = tripJson["time"]
         tripBoolean = price and date and time

         contactName = contactJson["name"]
         contactEmail = contactJson["email"]
         contactPhone = contactJson["phone"]
         contactBoolean = contactName and contactEmail and contactPhone
         userId = int(session["user"]["id"])

         if not (tripBoolean and attractionBoolean and contactBoolean and userId):
            return jsonify({ "error": True, "message": "訂單建立失敗，輸入不正確或其他原因" })
         
         if userId in range(1, 10):
            userIdInOrder = f"00{userId}"
         if userId in range(10, 100):
            userIdInOrder = f"0{userId}"
         tz = timezone(timedelta(hours = +8))
         orderNumber = datetime.strftime(datetime.now(tz), "%Y%m%d%H%M%S") + f"-{userIdInOrder}"
         
         insertOrder(attractionId = attractionId, userId = userId, phone = contactPhone, number = orderNumber, price = price, date = date, time = time, status = 1)

         insertedOrder = selectOrder(orderNumber, userId)
         # print("訂單編號成立:",orderNumber)
         
         if not insertedOrder:
            return jsonify({ "error": True, "message": "訂單建立失敗，輸入不正確或其他原因" })
         
         # 取得 prime API
         # 將PRIME取得後傳到後端
         payByPrime_Url = "https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime"
         headers = {
            "Content-Type": "application/json",
            "x-api-key": os.getenv("PARTNER_KEY")
         }
         tappayRequest = json.dumps({
            "prime": prime,
            "partner_key": os.getenv("PARTNER_KEY"),
            "merchant_id": "random_ESUN",
            "details": "Tappay test",
            "amount": price,
            "cardholder": {
               "phone_number": contactPhone,
               "name": contactName,
               "email": contactEmail,
               "zip_code": "",
               "address": "",
               "nation_id": "",
            }
         })
         # print("tappay::",tappayRequest)

         response = requests.post(payByPrime_Url, data = tappayRequest, headers = headers, timeout = 30)
         
         res = response.json()
         # print("res回復:",res)




         if res["status"] == 0:
            updateOrder(orderNumber, status = res["status"])

            insertedOrder = selectOrder(orderNumber, userId)

            message = "付款成功"
            orderData = {
               "number": insertedOrder["number"],
               "payment": {
                  "status": insertedOrder["status"],
                  "message": message
               }
            }
            return jsonify({ "data": orderData })
         else:
            message = "付款失敗"
            orderData = {
               "number": insertedOrder["number"],
               "payment": {
                  "status": insertedOrder["status"],
                  "message": message         
               }
            }
            return jsonify({ "data": orderData })
      else:
         return jsonify({ "error": True, "message": "請先登入" })
   except Exception as e:
      print(e)
      return jsonify({ "error": True, "message": "伺服器內部錯誤" })

@api_order.route("/order/<string:number>", methods=["GET"])
def getOrder(number):
   try:
      if "user" in session:
         userId = session["user"]["id"]
         selectedOrder = selectOrder(number, userId)

         if selectedOrder:
            orderData = {
               "number": number,
               "price": int(selectedOrder["price"]),
               "trip": {
                  "attraction": {
                     "id": int(selectedOrder["attractionId"]),
                     "name": selectedOrder["attr_name"],
                     "address": selectedOrder["address"],
                     "image": json.loads(selectedOrder["images"])[0]
                  },
                  "date": datetime.strftime(selectedOrder["date"], "%Y-%m-%d"),
                  "time": selectedOrder["time"],
               },
               "contact": {
                  "name": selectedOrder["user_name"],
                  "email": selectedOrder["email"],
                  "phone": selectedOrder["phone"]
               },
               "status": int(selectedOrder["status"])
            }
            return jsonify({ "data": orderData })
         else:
            return jsonify({ "data": None })
      else:
         return jsonify({ "error": True, "message": "請先登入" })
   except Exception as e:
      print(e)
      return jsonify({ "error": True, "message": "伺服器內部錯誤" })

# Andy's api
@api_order.route("/orders", methods=["GET"])
def getOrders():
   try:
      if "user" in session:
         userId = session["user"]["id"]
         orderDataList = selectOrders(userId)

         if orderDataList:
            return jsonify({ "data": orderDataList })
         else:
            return jsonify({ "data": None })
      else:
         return jsonify({ "error": True, "message": "請先登入" })
   except Exception as e:
      print(e)
      return jsonify({ "error": True, "message": "伺服器內部錯誤" })