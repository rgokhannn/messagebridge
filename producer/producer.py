import pika
import redis
import os

def main():
    # Connect to RabbitMQ
    rabbitmq_host = os.getenv('RABBITMQ_HOST', 'rabbitmq')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
    channel = connection.channel()
    channel.queue_declare(queue='hello')

    # Connect to Redis
    redis_client = redis.StrictRedis(host='redis', port=6379, db=0)

    message = "Hello RabbitMQ with Redis!"
    redis_client.set('last_message', message)
    
    channel.basic_publish(exchange='', routing_key='hello', body=message)
    print(f" [x] Sent '{message}' and stored in Redis")

    connection.close()

if __name__ == "__main__":
    main()