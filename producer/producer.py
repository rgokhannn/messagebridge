import pika
import redis
import os
from dotenv import load_dotenv

load_dotenv()

def on_channel_closed(channel, reply_code, reply_text):
    print(f"Channel was closed: ({reply_code}) {reply_text}")

def main():
    # Connect to RabbitMQ
    rabbitmq_host = os.getenv('RABBITMQ_HOST', 'rabbitmq')
    rabbitmq_user = os.getenv('RABBITMQ_USER', 'rabbitmq_user')
    rabbitmq_pass = os.getenv('RABBITMQ_PASS', 'asd123')

    credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_pass)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=rabbitmq_host, credentials=credentials)
    )
    channel = connection.channel()

    # Shutdown listener ekleme
    channel.add_on_close_callback(on_channel_closed)

    # Queue oluşturma
    channel.queue_declare(queue='hello')

    # Connect to Redis
    redis_host = os.getenv('REDIS_HOST', 'redis')
    redis_password = os.getenv('REDIS_PASSWORD', 'asd123')
    
    redis_client = redis.StrictRedis(
        host=redis_host, port=6379, password=redis_password, db=0, decode_responses=True
    )

    message = "Hello RabbitMQ with Redis!"
    redis_client.set('last_message', message)
    
    # Mesajı RabbitMQ'ye gönderme
    channel.basic_publish(exchange='', routing_key='hello', body=message)
    print(f" [x] Sent '{message}' and stored in Redis")

    # Bağlantıyı kapatma
    connection.close()

if __name__ == "__main__":
    main()