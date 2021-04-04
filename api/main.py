from marshmallow import Schema, fields, ValidationError
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
import pandas as pd
from json import loads
from bson.json_util import dumps
from datetime import datetime

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb+srv://shev:shevaunebrown7@cluster0.niden.mongodb.net/lab3?retryWrites=true&w=majority"
mongo = PyMongo(app)

ProfileDB = {
        "success": True,
        "data": {
            "last_updated": "2/3/2021, 8:48:51 PM",
            "username": "Silva",
            "role": "Engineer",
            "color": "blue"
        }
    }


class TankSchema(Schema):
    
    longitude = fields.String(required=True)
    latitude  = fields.String(required=True)
    location = fields.String(required=True)
    percentage_full = fields.Integer(required=True)

class Level(Schema):
    tank_id = fields.Integer(required=True)
    percentage_full = fields.Integer(required=True)

@app.route("/")
def home():
    return "ECSE3038-Lab 6"

# This section returns the data in the database
@app.route("/profile", methods=["GET", "POST", "PATCH"])
def get_profile():
    if request.method == "GET":
        return jsonify(ProfileDB)

    elif request.method == "POST":
        
        # This section returns the current time
        
        nw = datetime.nw()
        dte = nw.strftime("%d/%m/%Y %H:%M:%S")

        ProfileDB["data"]["last_updated"] = (dte)
        ProfileDB["data"]["username"] = (request.json["username"])
        ProfileDB["data"]["role"] = (request.json["role"])
        ProfileDB["data"]["color"] = (request.json["color"])

        return jsonify(ProfileDB)

    elif request.method == "PATCH":
       
       # This section returns the current time 
        
        nw = datetime.nw()
        dte = nw.strftime("%d/%m/%Y %H:%M:%S")
    
        data = ProfileDB["data"]

        a = request.json
        a["last_updated"] = dte
        attributes = a.keys()
        for attribute in attributes:
            data[attribute] = a[attribute]

        return jsonify(ProfileDB)    


# This section returns all the data in TANK_DB
@app.route("/data", methods=["GET", "POST"])
def tank_data():
    if request.method == "GET":
        tanks = mongo.db.tanks.find()
        return jsonify(loads(dumps(tanks)))  
    elif request.method == "POST":
        try:
            tank = TankSchema().load(request.json)
            mongo.db.tanks.insert_one(tank)
            return loads(dumps(tank))
        except ValidationError as e:
            return e.messages, 400   
 
@app.route('/data/<ObjectId:id>', methods=["PATCH", "DELETE"])
def tank_id_methods(id):
    if request.method == "PATCH":
        mongo.db.tanks.update_one({"_id": id}, {"$set": request.json})

        tank = mongo.db.tanks.find_one(id)
        
        return loads(dumps(tank))    
    elif request.method == "DELETE":
        result = mongo.db.tanks.delete_one({"_id": id})

        if result.deleted_count == 1:
            return {
                "success": True
            }
        else:
            return {
                "success": False
            }, 400

def map(val, fromLow, fromHigh, toLow, toHigh):
    return int(((val - fromLow) * (toHigh - toLow))/((fromHigh - fromLow) + toLow))

@app.route("/tank", methods=["POST"])
def post_tank_level():
    try:
        tank_id = request.json["tank_id"]
        water_level = request.json["water_level"]
        percentage_full = map(water_level, 200, 10, 0, 100)

        jsonBody = {
            "tank_id": tank_id,
            "percentage_full": percentage_full
        }

        tank_level = Level().load(jsonBody)
        mongo.db.levels.insert_one(tank_level)

        nw = datetime.nw()
        dte = nw.strftime("%d/%m/%Y %H:%M:%S")

        return {
            "success": True,
            "msg": "data saved ",
            "date": dte
        }
    except ValidationError as e:
        return e.messages, 400           


if __name__ == "__main__":
    app.run(
        debug=True,
        host="192.168.1.4",
        port=5000
    )
