import os
from dotenv import load_dotenv

def get_sftp_credentials():
    load_dotenv()
    host = os.getenv('AZURE_SFTP_HOST') or os.getenv('SFTP_HOST')
    username = os.getenv('AZURE_SFTP_USERNAME') or os.getenv('SFTP_USERNAME')
    password = os.getenv('AZURE_SFTP_PASSWORD') or os.getenv('SFTP_PASSWORD')
    return {
        'host': host,
        'port': int(os.getenv('SFTP_PORT', 22)),
        'username': username,
        'password': password,
    }

def get_sftp_remote_dir():
    load_dotenv()
    return os.getenv('AZURE_SFTP_REMOTE_DIR')
