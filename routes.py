from flask import Blueprint, render_template, session, redirect, url_for, jsonify, current_app
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html') if 'credentials' in session else render_template('login.html')

@main.route('/login')
def login():
    google = current_app.config['google']
    redirect_uri = url_for('main.authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@main.route('/oauth2callback')
def authorize():
    google = current_app.config['google']
    token = google.authorize_access_token()
    resp = google.get('userinfo', token=token)
    user_info = resp.json()
    session['email'] = user_info['email']
    session['credentials'] = token
    return redirect(url_for('main.index'))

@main.route('/api/files')
def files():
    if 'credentials' not in session:
        return redirect(url_for('main.login'))

    google = current_app.config['google']
    credentials = google.oauth.create_client('google').token_from_raw(session['credentials'])

    try:
        if credentials.expired:
            credentials.refresh(Request())

        drive_service = build('drive', 'v3', credentials=credentials)
        results = drive_service.files().list(
            pageSize=10,
            fields="nextPageToken, files(id, name, size, modifiedTime)"
        ).execute()

        items = results.get('files', [])
        if not items:
            return jsonify([]), 404
        else:
            files_info = [{'name': item['name'],
                           'size': item.get('size', 'Unknown size'),
                           'last_modified': item['modifiedTime']} for item in items]
            return jsonify(files=files_info)
    except Exception as e:
        return str(e), 500
