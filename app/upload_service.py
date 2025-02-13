
from flask import Flask, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_uploads import UploadSet, configure_uploads, VIDEOS
import pika
import os
import uuid
import json

app = Flask(__name__)
app.config['UPLOADED_VIDEOS_DEST'] = 'uploads'
videos = UploadSet('videos', VIDEOS)
configure_uploads(app, videos)

@app.route('/upload', methods=['POST'])
@jwt_required()
def upload_video():
    current_user = get_jwt_identity()
    video_file = request.files.get('file')
    if not video_file:
        return jsonify(message="No file uploaded"), 400

    # Create unique filename to avoid conflicts
    filename = str(uuid.uuid4()) + ".mp4"
    file_path = os.path.join(app.config['UPLOADED_VIDEOS_DEST'], filename)
    video_file.save(file_path)

    # Send message to RabbitMQ Gate service
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='gate_queue')

    # Construct message to be sent to Gate Service
    message = {
        'video_path': file_path,
        'user': current_user,
        'formats': ['mp3', '360p', '144p']  # You can add more formats/resolutions here
    }
    channel.basic_publish(exchange='', routing_key='gate_queue', body=json.dumps(message))
    connection.close()

    return jsonify(message="File uploaded successfully", filename=filename), 201

if __name__ == '__main__':
    app.run(debug=True)
