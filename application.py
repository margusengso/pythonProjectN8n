import os
from flask import Flask, jsonify, Response, request
from flask_socketio import SocketIO, send
from dotenv import load_dotenv
import requests

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('WS_SECRET_KEY')

# Initialize SocketIO with gevent
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="gevent")


@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Hello n8n project'})


@app.route('/proxy-audio', methods=['GET'])
def proxy_audio():
    file_id = request.args.get('file_id')
    google_drive_url = f"https://drive.google.com/uc?export=download&id={file_id}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(google_drive_url, headers=headers, stream=True)
    if response.status_code == 200:
        return Response(
            response.iter_content(chunk_size=1024),
            content_type='audio/mpeg',
            headers={'Content-Disposition': 'inline'}
        )
    else:
        return Response('Unable to fetch the audio file', status=400)


@socketio.on('message')
def handle_message(msg):
    print(f"Message received: {msg}")

    # Use the received message as the file ID if that's the format you're expecting
    file_id = msg.strip()

    # Construct the proxy URL using the file ID
    proxy_url = f"https://pythonprojectn8n.onrender.com/proxy-audio?file_id={file_id}"

    # Reply with the proxy URL included
    reply = f"Server says: You sent '{msg}'. Audio URL: {proxy_url}"
    send(reply)


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))
    socketio.run(app, debug=True, host='0.0.0.0', port=port)