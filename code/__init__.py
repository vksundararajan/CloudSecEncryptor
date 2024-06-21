from flask import Flask
from .routes import main
import os


def create_app():
    app = Flask(__name__)
    app.secret_key = os.urandom(16)

    from authlib.integrations.flask_client import OAuth
    oauth = OAuth(app)

    app.config['google'] = oauth.register(
        name='google',
        client_id='your_client_id',
        client_secret='your_client_secret',
        access_token_url='https://accounts.google.com/o/oauth2/token',
        authorize_url='https://accounts.google.com/o/oauth2/auth',
        api_base_url='https://www.googleapis.com/oauth2/v1/',
        client_kwargs={'scope': 'https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/drive'},
    )

    app.register_blueprint(main)
    return app
