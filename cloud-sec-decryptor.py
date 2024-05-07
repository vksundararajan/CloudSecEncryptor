from googleapiclient.http import MediaIoBaseDownload
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import io
import os
import base64
import pickle
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

def create_service():
    """Creates a Google Drive service object via OAuth authentication."""
    SCOPES = ['https://www.googleapis.com/auth/drive']
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('drive', 'v3', credentials=creds)
    return service

def find_file_id_by_name(service, filename):
    """Retrieves the file ID for a given filename in Google Drive."""
    query = f"name='{filename}'"
    results = service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
        return None
    return items[0]['id']

def download_file(service, filename):
    """Downloads a file from Google Drive by filename."""
    file_id = find_file_id_by_name(service, filename)
    if not file_id:
        raise FileNotFoundError("File not found on Google Drive.")
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
        print(f"Download progress: {status.progress() * 100:.2f}%")
    fh.seek(0)
    return fh.read()

def decrypt_file(encrypted_data, key):
    """Decrypts AES encrypted data using a given key."""
    try:
        iv = base64.b64decode(encrypted_data[:24])
        ct = base64.b64decode(encrypted_data[24:])
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = unpad(cipher.decrypt(ct), AES.block_size)
        return plaintext
    except ValueError as e:
        raise SecurityError("Decryption failed. Check key or data integrity.") from e

class SecurityError(Exception):
    """Exception raised for errors in the decryption process."""
    pass

def save_decrypted_file(plaintext, filename):
    """Saves decrypted data to a file, removing '.encrypted' from the filename if present."""
    original_filename = filename.replace('.encrypted', '')
    with open(original_filename, 'wb') as f:
        f.write(plaintext)
    print(f"Decrypted file saved as: {original_filename}")

if __name__ == '__main__':
    service = create_service()
    filename = 'sample-data.txt'
    try:
        encrypted_data = download_file(service, filename)
        key = base64.b64decode('YOUR_KEY_BASE64')  # Replace YOUR_KEY_BASE64 with your actual base64-encoded AES key
        plaintext = decrypt_file(encrypted_data, key)
        save_decrypted_file(plaintext, filename)
    except SecurityError as error:
        print(f"Security error: {error}")
    except FileNotFoundError as e:
        print(f"Error: {e}")
