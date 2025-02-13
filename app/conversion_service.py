
import pika
import os
import subprocess
import json
from flask import Flask

app = Flask(__name__)

# Helper function to convert the video to different formats
def convert_video(video_path, output_format, resolution=None):
    output_file = None
    if output_format == 'mp3':
        output_file = video_path.replace('.mp4', '.mp3')
        subprocess.run(['ffmpeg', '-i', video_path, '-vn', output_file])
    elif resolution:
        output_file = video_path.replace('.mp4', f'_{resolution}.mp4')
        subprocess.run(['ffmpeg', '-i', video_path, '-vf', f'scale={resolution}', output_file])
    else:
        output_file = video_path.replace('.mp4', f'_{output_format}.mp4')
        subprocess.run(['ffmpeg', '-i', video_path, output_file])
    
    return output_file

# Callback function to handle messages from Gate Service
def on_message(ch, method, properties, body):
    message = json.loads(body.decode())
    video_path = message['video_path']
    user = message['user']
    formats = message['formats']

    # Folder for converted files
    output_folder = os.path.join('converted', user)
    os.makedirs(output_folder, exist_ok=True)

    # Convert the video into requested formats
    converted_files = []
    for format in formats:
        if format == 'mp3':
            converted_file = convert_video(video_path, 'mp3')
        elif format == '360p':
            converted_file = convert_video(video_path, 'mp4', '640x360')
        elif format == '144p':
            converted_file = convert_video(video_path, 'mp4', '256x144')
        converted_files.append(converted_file)
    
    # Move the converted files to the output folder
    for converted_file in converted_files:
        os.rename(converted_file, os.path.join(output_folder, os.path.basename(converted_file)))
    
    print(f"Conversion complete for user {user}: {converted_files}")

def start_conversion_service():
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='video_conversion_queue')

    # Start consuming messages
    channel.basic_consume(queue='video_conversion_queue', on_message_callback=on_message, auto_ack=True)
    print("Video Conversion service is running...")
    channel.start_consuming()

if __name__ == '__main__':
    start_conversion_service()
