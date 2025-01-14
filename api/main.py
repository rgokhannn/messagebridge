from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pika
import redis
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Redis configuration
redis_host = os.getenv('REDIS_HOST', 'redis')
redis_password = os.getenv('REDIS_PASSWORD', 'your_redis_password')
redis_client = redis.StrictRedis(host=redis_host, port=6379, db=0)

# MongoDB configuration
mongo_user = os.getenv('MONGO_USER', 'myUser')
mongo_pass = os.getenv('MONGO_PASS', 'myPassword')
mongo_host = os.getenv('MONGODB_HOST', 'mongodb')
mongo_client = MongoClient(f'mongodb://{mongo_host}:27017/')
mongo_db = mongo_client.my_database
mongo_collection = mongo_db.messages

class Message(BaseModel):
    message: str

@app.post("/send")
def send_message(msg: Message):
    message = msg.message
    rabbitmq_user = os.getenv('RABBITMQ_USER', 'rabbitmq_user')
    rabbitmq_pass = os.getenv('RABBITMQ_PASS', 'your_rabbitmq_password')
    rabbitmq_host = os.getenv('RABBITMQ_HOST', 'rabbitmq')

    credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_pass)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host, 5672, '/', credentials=credentials))
    channel = connection.channel()
    channel.queue_declare(queue='hello')
    channel.basic_publish(exchange='', routing_key='hello', body=message)
    connection.close()

    redis_client.set('last_message', message)
    return {"status": "Message sent and stored in Redis", "message": message}

@app.get("/redis")
def get_redis_data():
    message = redis_client.get('last_message')
    if message:
        return {"last_message": message.decode()}
    else:
        raise HTTPException(status_code=404, detail="No message found in Redis")

@app.get("/mongodb")
def get_mongo_data():
    messages = list(mongo_collection.find({}, {'_id': 0, 'message': 1}))
    return {"messages": messages}