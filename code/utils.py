import os
from cryptography.fernet import Fernet, InvalidToken
from dotenv import load_dotenv
from oauth.login import get_drive_service, isLoggedIn


load_dotenv()   # looks for .env in cwd by default


def load_crypt_key() -> bytes:
  key = os.getenv("CRYPT_KEY")
  if not key:
    raise RuntimeError("CRYPT_KEY not set in environment (.env).")
  # if stored as plain text without b'' this returns str; Fernet expects bytes
  if isinstance(key, str):
      key = key.encode('utf-8')
  return key


def encrypt_bytes_from_file(path: str, key: bytes) -> bytes:
  with open(path, "rb") as f:
    plaintext = f.read()
  fernet = Fernet(key)
  ciphertext = fernet.encrypt(plaintext)
  return ciphertext


def decrypt_bytes_to_file(ciphertext: bytes, out_path: str, key: bytes) -> None:
  fernet = Fernet(key)
  try:
      plaintext = fernet.decrypt(ciphertext)
  except InvalidToken:
      raise ValueError("Decryption failed: invalid key or corrupted ciphertext.")
  os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
  with open(out_path, "wb") as f:
    f.write(plaintext)


def list_all_files():
  if not isLoggedIn():
    return False

  service = get_drive_service()
  page_token = None
  while True:
    response = service.files().list(
      fields="nextPageToken, files(id, name, mimeType)",
      pageToken=page_token
    ).execute()
    for file in response.get('files', []):
      print(f"{file['name']} ({file['id']}) - {file['mimeType']}")
    page_token = response.get('nextPageToken', None)
    if page_token is None:
      break
