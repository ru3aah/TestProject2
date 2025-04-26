"""
Settings module for the image hosting server.

This module contains global settings for the server, such as the address to
listen on, the paths to the static files and uploaded images, and the
maximum allowed file size.

Attributes:
    SERVER_ADDRESS (tuple): The address to listen on.
    STATIC_PATH (str): The path to the static files.
    IMAGES_PATH (str): The path to the uploaded images.
    ALLOWED_EXTENSIONS (list): The list of allowed file extensions.
    MAX_FILE_SIZE (int): The maximum allowed file size in bytes.
    LOG_PATH (str): The path to the log files.
"""

import os

import dotenv

dotenv.load_dotenv('.env')
SERVER_ADDRESS = ('0.0.0.0', 8000)
STATIC_PATH = 'static/'
IMAGES_PATH = 'images/'
ALLOWED_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif']
MAX_FILE_SIZE = 5 * 1024 * 1024
LOG_PATH = 'logs/'
LOG_FILE = 'app.log'
PAGE_LIMIT = 10
ERROR_FILE = 'upload_failed.html'

DB_NAME = os.getenv('DB_NAME') or 'postgres'
DB_USER = os.getenv('DB_USER') or 'postgres'
DB_PASSWORD = os.getenv('DB_PASSWORD') or 'postgres'
DB_HOST = os.getenv('DB_HOST') or 'db'
DB_PORT = os.getenv('DB_PORT') or '5432'