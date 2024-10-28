import os
from flask import Flask, jsonify
from flask_socketio import SocketIO, send
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

@socketio.on('message')
def handle_message(msg):
    print(f"Message received: {msg}")
    reply = f"Server says: You sent '{msg}'"
    send(reply)

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))
    socketio.run(app, debug=True, host='0.0.0.0', port=port)