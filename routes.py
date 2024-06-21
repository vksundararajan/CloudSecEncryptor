from flask import Blueprint, render_template, session, redirect, url_for, jsonify, current_app, send_file
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.errors import HttpError
from .utils.auth_utils import get_google_credentials
import io

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
    try:
        google = current_app.config['google']
        token = google.authorize_access_token()
        resp = google.get('userinfo', token=token)
        user_info = resp.json()
        session['email'] = user_info['email']
        session['credentials'] = token
        return redirect(url_for('main.index'))
    except Exception as e:
        current_app.logger.error(f"Failed to process OAuth callback: {str(e)}")
        return f"An error occurred: {str(e)}", 500


@main.route('/delete/<file_id>', methods=['POST'])
def delete_file(file_id):
    credentials = get_google_credentials()
    if not credentials:
        return redirect(url_for('main.login')), 401
    try:
        drive_service = build('drive', 'v3', credentials=credentials)
        response = drive_service.files().delete(fileId=file_id).execute()
        return jsonify({'message': 'File deleted successfully'}), 200
    except HttpError as error:
        error_content = error.resp.reason
        return jsonify({'error': 'Google API error', 'details': error_content}), error.resp.status
    except Exception as e:
        current_app.logger.error(f"Unexpected error: {str(e)}")
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@main.route('/download/<file_id>')
def download_file(file_id):
    credentials = get_google_credentials()
    if not credentials:
        return redirect(url_for('main.login')), 401
    try:
        drive_service = build('drive', 'v3', credentials=credentials)
        file_metadata = drive_service.files().get(fileId=file_id, fields='name, mimeType').execute()
        file_name = file_metadata.get('name', 'downloaded_file')
        mime_type = file_metadata.get('mimeType', 'application/octet-stream')
        request = drive_service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            _, done = downloader.next_chunk()
        fh.seek(0)
        return send_file(
            fh,
            as_attachment=True,
            download_name=file_name,
            mimetype=mime_type
        )
    except HttpError as error:
        return jsonify({'error': str(error)}), error.resp.status
    except Exception as e:
        current_app.logger.error(f"Unexpected error: {str(e)}")
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@main.route('/api/files')
def files():
    if 'credentials' not in session:
        return redirect(url_for('main.login'))
    creds_info = session['credentials']
    credentials = get_google_credentials()
    if credentials and credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())
    try:
        drive_service = build('drive', 'v3', credentials=credentials)
        results = drive_service.files().list(
            pageSize=100,
            fields="nextPageToken, files(id, name, mimeType, size, modifiedTime)"
        ).execute()
        items = results.get('files', [])
        if not items:
            return jsonify({'message': 'No files found.'}), 404
        files_info = [{
            'fileName': file.get('name'),
            'fileId': file['id'],
            'size': f"{int(file.get('size', 0)) / 1024:.2f} KB" if file.get('size') else 'Unknown size',
            'lastModified': file.get('modifiedTime', 'Unknown time')
        } for file in items]
        return jsonify(files=files_info)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@main.route('/api/upload', methods=['POST'])
def upload_files():
    key = load_key('path_to_key.key')
    files = request.files.getlist("file")
    drive_service = build('drive', 'v3', credentials=get_google_credentials())
    for file in files:
        file_data = file.read()
        encrypted_data = encrypt_data(file_data, key)
        temp_file_path = file.filename + '.enc'
        with open(temp_file_path, 'wb') as temp_file:
            temp_file.write(encrypted_data)
        file_metadata = {'name': temp_file_path}
        media = MediaFileUpload(temp_file_path, mimetype='application/octet-stream')
        file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        os.remove(temp_file_path)
    return jsonify({'message': 'Files uploaded successfully'})
