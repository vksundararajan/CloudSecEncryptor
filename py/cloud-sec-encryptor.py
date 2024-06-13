import os
import pickle
import base64
import io
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseUpload
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

# Define the scope for Google Drive API
SCOPES = ['https://www.googleapis.com/auth/drive']

# Load or refresh existing credentials
creds = None
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)
service = build('drive', 'v3', credentials=creds)

def encrypt_file(filename, key):
    """Encrypts a file using AES encryption with CBC mode and returns the IV and ciphertext."""
    with open(filename, 'rb') as f:
        data = f.read()
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(data, AES.block_size))
    iv = base64.b64encode(cipher.iv).decode('utf-8')
    ct = base64.b64encode(ct_bytes).decode('utf-8')
    return iv, ct

def upload_to_drive(filename, iv, ct):
    """Uploads an encrypted file to Google Drive, combining the IV and ciphertext into a single file."""
    body = {'name': filename, 'mimeType': 'text/plain'}
    encoded_text = iv + ct
    media = io.BytesIO(encoded_text.encode('utf-8'))
    media_upload = MediaIoBaseUpload(media, mimetype='text/plain', resumable=True)
    file = service.files().create(body=body, media_body=media_upload, fields='id').execute()
    print('File ID:', file.get('id'))

if __name__ == '__main__':
    # Example usage with a hardcoded key
    key = base64.b64decode('YOUR_KEY_BASE64')  # Replace YOUR_KEY_BASE64 with your actual base64-encoded AES key
    iv, ct = encrypt_file('sample-data.txt', key)
    upload_to_drive('sample-data.txt', iv, ct)
