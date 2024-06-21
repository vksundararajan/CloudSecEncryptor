from flask import session, current_app
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

def get_google_credentials():
    if 'credentials' not in session:
        return None

    creds_info = session['credentials']
    credentials = Credentials(
        token=creds_info.get('access_token'),
        refresh_token=creds_info.get('refresh_token'),
        token_uri='https://oauth2.googleapis.com/token',
        client_id=current_app.config['google'].client_id,
        client_secret=current_app.config['google'].client_secret,
        scopes=['https://www.googleapis.com/auth/drive']
    )

    if credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())
    
    return credentials
