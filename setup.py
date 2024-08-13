from flask import Flask
from db import db
from utils.mailer import mail
# import requests
from flask_cors import CORS
from dotenv import load_dotenv
from os import getenv, path

# load env variables
load_dotenv()


base_dir = path.abspath(path.dirname(__name__))
db_path = path.join(base_dir, getenv('DB_NAME'))

def create_app():
    app = Flask(__name__)
    app.secret_key = getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['MAIL_SERVER'] = getenv('MAIL_SERVER')
    app.config['MAIL_PORT'] = getenv('MAIL_PORT')
    app.config['MAIL_USERNAME'] = getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = getenv('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = getenv('MAIL_DEFAULT_SENDER')

    db.init_app(app)
    mail.init_app(app)
    
    # Enabling cross-origin requests
    cors = CORS()
    cors.init_app(app)

    return app
