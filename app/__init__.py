import os
from flask import Flask
from flask_socketio import SocketIO
from flask_apscheduler import APScheduler
from dotenv import load_dotenv
from .sockets import init_sockets

load_dotenv()

socketio = SocketIO(cors_allowed_origins="*", async_mode="gevent")
scheduler = APScheduler()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('WS_SECRET_KEY', 'default_secret')
    app.config['SCHEDULER_API_ENABLED'] = True

    socketio.init_app(app)
    scheduler.init_app(app)
    scheduler.start()

    from .routes import bp as routes_bp
    from .sockets import init_sockets

    app.register_blueprint(routes_bp)
    init_sockets(socketio)

    return app