import pika
import redis
import os
from dotenv import load_dotenv

load_dotenv()

def main():
    # Connect to RabbitMQ
    rabbitmq_host = 'rabbitmq'
    rabbitmq_user = 'rabbitmq_user'
    rabbitmq_pass = 'asd123'

    credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_pass)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=rabbitmq_host, credentials=credentials)
    )
    channel = connection.channel()
    channel.queue_declare(queue='hello')

    # Connect to Redis
    redis_host = os.getenv('REDIS_HOST', 'redis')
    redis_password = os.getenv('REDIS_PASSWORD', 'asd123')
    redis_client = redis.StrictRedis(host=redis_host, port=6379, password='asd123', db=0, decode_responses=True)

    message = "Hello RabbitMQ with Redis!"
    redis_client.set('last_message', message)
    
    channel.basic_publish(exchange='', routing_key='hello', body=message)
    print(f" [x] Sent '{message}' and stored in Redis")

    connection.close()

if __name__ == "__main__":
    main()