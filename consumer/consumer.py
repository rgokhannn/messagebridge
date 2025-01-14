import pika
from pymongo import MongoClient
import os

def callback(ch, method, properties, body):
    print(f" [x] Received {body}")

    # Store the message to MongoDB
    mongo_user = os.getenv('MONGO_USER', 'myUser')
    mongo_pass = os.getenv('MONGO_PASS', 'myPassword')
    mongo_host = os.getenv('MONGODB_HOST', 'mongodb')
    client = MongoClient(f'mongodb://{mongo_host}:27017/')
    db = client.my_database
    collection = db.messages
    collection.insert_one({"message": body.decode()})
    print(" [x] Message stored in MongoDB")

def main():
    # Connect to RabbitMQ
    rabbitmq_host = os.getenv('RABBITMQ_HOST', 'rabbitmq')
    rabbitmq_user = os.getenv('RABBITMQ_USER', 'rabbitmq_user')
    rabbitmq_pass = os.getenv('RABBITMQ_PASS', 'your_rabbitmq_password')

    credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_pass)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=rabbitmq_host, credentials=credentials)
    )
    channel = connection.channel()
    channel.queue_declare(queue='hello')

    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == "__main__":
    main()