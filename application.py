import gevent.monkey
gevent.monkey.patch_all()  # Ensure this is the first thing done in your code!

import os
from flask import Flask
from flask_socketio import SocketIO
from dotenv import load_dotenv
from app.sockets import message_received
from app.routes import init_routes

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('WS_SECRET_KEY')

socketio = SocketIO(app, cors_allowed_origins="*", async_mode="gevent")

init_routes(app)

@socketio.on('message')
def handle_message(msg):
    message_received(msg)


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))
    socketio.run(app, debug=True, host='0.0.0.0', port=port)

