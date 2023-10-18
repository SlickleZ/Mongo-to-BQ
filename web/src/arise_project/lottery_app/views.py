from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from random import randint
from datetime import datetime
from pytz import timezone
from pymongo.mongo_client import MongoClient
from pymongo.errors import PyMongoError


def index(req):
    return render(req, "index.html")

def rand_number_and_save(req, user_name):
    if user_name.lstrip() == "Username":
        return JsonResponse({"status": 400, "message": "Please select the username"}, status=400)
    
    rand_number = format(randint(000000,999999), "06d")
    bangkok_tz = timezone("Asia/Bangkok")
    
    res = {
        "status": 200,
        "user_name": user_name,
        "rand_number": rand_number
    }
    
    try:
        client = MongoClient("mongodb://mongodb:27017/?replicaSet=rs0")
        data_to_load = {
            "user_name": user_name,
            "lottery_number": rand_number,
            "created_timestamp": datetime.now(tz=bangkok_tz)
        }
        # print(data_to_load)
        client.admin.command("ping")
        db = client.get_database(name="lottery")
        load_result = db.logs.insert_one(data_to_load)
    except PyMongoError as e:
        print(e)

    return JsonResponse(res, status=200)

def like_and_dislike(req, user_name, lottery_number, preference):
    bangkok_tz = timezone("Asia/Bangkok")
    res = {
        "user_name": user_name,
        "lottery_number": lottery_number,
        "preference": preference
    }
    
    try:
        client = MongoClient("mongodb://mongodb:27017/?replicaSet=rs0")
        data_to_load = {
            "user_name": user_name,
            "lottery_number": lottery_number,
            "preference": int(preference),
            "event_timestamp": datetime.now(tz=bangkok_tz)
        }
        # print(data_to_load)
        client.admin.command("ping")
        db = client.get_database(name="lottery")
        load_result = db.preference.insert_one(data_to_load)
    except PyMongoError as e:
        print(e)

    return JsonResponse(res, status=200)