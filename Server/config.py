import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-123'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///monitoring.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CPU_ALERT_THRESHOLD = 40.0
    MEMORY_ALERT_THRESHOLD = 75.0
    SERVER_HOST = '0.0.0.0'
    SERVER_PORT = 5000