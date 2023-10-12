from kafka import KafkaProducer
from pymongo.mongo_client import MongoClient
from pymongo.errors import PyMongoError
import logging
import json
from bson.json_util import dumps


_logger = logging.getLogger(__name__)
producer = KafkaProducer(bootstrap_servers=["broker:29092"],
                         value_serializer=lambda v: json.dumps(v).encode("utf-8"))
client = MongoClient('mongodb://mongodb:27017/?replicaSet=rs0')
pipeline = [{
    "$match": {
        "operationType": { "$in": ["insert"] }
    }
}]
resume_token = None


if __name__ == "__main__":
    try:
        client.admin.command('ping')
        db = client.get_database(name='lottery')

        with db.preference.watch(pipeline=pipeline) as stream:
            _logger.info('Producer is currently watching ...')
            
            for change in stream:
                json_change = json.loads(dumps(change))
                producer.send("lottery.preference", json_change.get('fullDocument'))
                resume_token = stream.resume_token
    except PyMongoError:
        if resume_token is None:
            _logger.error("There is no usable resume token because there was a failure during ChangeStream initialization.")
        else:
            with db.preference.watch(pipeline=pipeline, resume_after=resume_token) as stream:
                _logger.info('Producer is currently watching ...')
                
                for change in stream:
                    json_change = json.loads(dumps(change))
                    producer.send("lottery.preference", json_change.get('fullDocument'))