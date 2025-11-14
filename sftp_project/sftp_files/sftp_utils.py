import os
from dotenv import load_dotenv

def get_sftp_credentials():
    load_dotenv()
    return {
        'host': os.getenv('SFTP_HOST'),
        'port': int(os.getenv('SFTP_PORT', 22)),
        'username': os.getenv('SFTP_USERNAME'),
        'password': os.getenv('SFTP_PASSWORD'),
    }
