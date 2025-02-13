
import pika
import json
import os

# Helper function to forward message to Video Conversion Service
def forward_to_conversion_service(message):
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='video_conversion_queue')

    channel.basic_publish(exchange='', routing_key='video_conversion_queue', body=json.dumps(message))
    connection.close()

# Callback function to handle messages from Upload Service
def on_message(ch, method, properties, body):
    message = json.loads(body.decode())
    video_path = message['video_path']
    user = message['user']
    formats = message['formats']
    
    # Forward the message to the conversion service
    message_for_conversion = {
        'video_path': video_path,
        'user': user,
        'formats': formats
    }
    forward_to_conversion_service(message_for_conversion)
    print(f"Message forwarded to conversion service: {message_for_conversion}")

def start_gate_service():
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='gate_queue')

    # Start consuming messages
    channel.basic_consume(queue='gate_queue', on_message_callback=on_message, auto_ack=True)
    print("Gate service is running...")
    channel.start_consuming()

if __name__ == '__main__':
    start_gate_service()
