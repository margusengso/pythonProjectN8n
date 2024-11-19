import os

class Config:
    SECRET_KEY = os.getenv('WS_SECRET_KEY', 'default_secret')
    SCHEDULER_API_ENABLED = True