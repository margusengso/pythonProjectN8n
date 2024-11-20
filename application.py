import gevent.monkey
gevent.monkey.patch_all()  # Ensure this is the first thing done in your code!

import os
from flask import Flask
from flask_socketio import SocketIO
from dotenv import load_dotenv
# from app.tasks import job1
from app.sockets import message_received
from app.routes import init_routes
# import schedule

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('WS_SECRET_KEY')


# Initialize SocketIO with gevent
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="gevent")

# schedule.every(1).minutes.do(job1)

init_routes(app)


@socketio.on('message')
def handle_message(msg):
    message_received(msg)



if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))
    socketio.run(app, debug=True, host='0.0.0.0', port=port)

