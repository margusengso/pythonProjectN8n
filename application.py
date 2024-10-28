import gevent.monkey
gevent.monkey.patch_all()  # Ensure this is the first thing done in your code!

import os
import requests
from flask import Flask, jsonify, Response, request
from flask_socketio import SocketIO, emit
from dotenv import load_dotenv

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

    # Send the message to the n8n webhook
    n8n_url = "https://margusengso.app.n8n.cloud/webhook/703b38d1-2ba1-45ad-86d2-458031dc1e4f"
    headers = {
        "Content-Type": "application/json"
    }
    try:
        # Make the POST request to n8n with headers
        response = requests.post(n8n_url, json={"the_text": msg}, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()

            # Since the response is a list, access the first element
            if isinstance(data, list) and len(data) > 0:
                file_info = data[0]  # Get the first item from the list
                file_id = file_info.get("id")
                if file_id:
                    proxy_url = f"https://pythonprojectn8n.onrender.com/proxy-audio?file_id={file_id}"
                    reply = {'status': 'success', 'url': proxy_url}
                    emit('response', reply)  # Emit the structured response to the client
                else:
                    emit('response', {'status': 'error', 'message': "No file ID found in the response."})
            else:
                emit('response', {'status': 'error', 'message': "Unexpected response format from n8n."})
        else:
            emit('response', {'status': 'error', 'message': f"Failed to get a response from n8n. Status code: {response.status_code}"})
    except Exception as e:
        emit('response', {'status': 'error', 'message': f"An error occurred: {str(e)}"})

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))
    socketio.run(app, debug=True, host='0.0.0.0', port=port)