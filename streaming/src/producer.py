from kafka import KafkaProducer
from pymongo.mongo_client import MongoClient
from pymongo.errors import PyMongoError
import json
from bson.json_util import dumps


producer = KafkaProducer(bootstrap_servers=["broker:29092"],
                         value_serializer=lambda v: json.dumps(v).encode("utf-8"))
client = MongoClient("mongodb://mongodb:27017/?replicaSet=rs0")
pipeline = [{
    "$match": {
        "operationType": { "$in": ["insert"] }
    }
}]
resume_token = None

try:
    client.admin.command("ping")
    db = client.get_database(name="lottery")

    with db.preference.watch(pipeline=pipeline) as stream:
        print("Producer is currently watching ...")
        
        for change in stream:
            json_change = json.loads(dumps(change))
            producer.send("lottery.preference", json_change.get("fullDocument"))
            print(f"Send data: {json_change.get('fullDocument')} to topic: lottery.preference successfully.")
            resume_token = stream.resume_token
except PyMongoError:
    if resume_token is None:
        print("There is no usable resume token because there was a failure during ChangeStream initialization.")
    else:
        with db.preference.watch(pipeline=pipeline, resume_after=resume_token) as stream:
            print("Producer is currently watching again ...")
            
            for change in stream:
                json_change = json.loads(dumps(change))
                producer.send("lottery.preference", json_change.get("fullDocument"))
                print(f"Send data: {json_change.get('fullDocument')} to topic: lottery.preference successfully.")