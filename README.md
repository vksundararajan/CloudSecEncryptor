# Cloud Sec Encryptor

## Description
**Cloud Sec Encryptor** is a Python-based application designed to securely encrypt and decrypt files using AES-256 encryption before uploading to or downloading from Google Drive. This ensures that your sensitive data remains protected both during transit and while at rest in the cloud. The project leverages Google Drive's API for storage operations, and the encryption mechanism is implemented using the Cryptography library.

## Features
- AES-256 encryption for files before upload.
- Secure decryption of downloaded files.
- Automatic retrieval of files by name instead of requiring file IDs.
- Local storage of decrypted files with original file names and types.
- Robust error handling for security and connectivity issues.

## Installation

### Prerequisites
- Python 3.6+
- Pip (Python package installer)

### Setup
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/Cloud-Sec-Encryptor.git
   cd Cloud-Sec-Encryptor
   ```

2. **Install Required Python Packages:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Google API Credentials:**
   - Visit the [Google Cloud Console](https://console.cloud.google.com/).
   - Create a new project and enable the Google Drive API.
   - Configure the OAuth consent screen and create OAuth 2.0 credentials.
   - Download the credentials JSON file and place it in the project directory.

### Configuration
- Rename the downloaded Google API credentials file to `credentials.json`.
- Ensure your file `token.pickle` is ready (generated during the first run).

## Usage

### Encrypting and Uploading Files
To encrypt a file and upload it to Google Drive:
1. Place the file in the project directory or specify the path.
2. Run the script with the appropriate command to encrypt and upload:
   ```bash
   python cloud_sec_encryptor.py upload <filename>
   ```

### Downloading and Decrypting Files
To download and decrypt a file from Google Drive:
1. Ensure you know the filename.
2. Run the script with the command to download and decrypt:
   ```bash
   python cloud_sec_encryptor.py download <encrypted_filename>
   ```

## Troubleshooting

### Common Issues
- **Invalid Credentials**: Ensure `credentials.json` is correct and that you have followed the Google API setup instructions.
- **Encryption Key Errors**: If decryption fails with a key error, check that you're using the correct key and that it matches the one used for encryption.
- **File Not Found**: Ensure the filename is correct and exists in your Google Drive.

### Error Handling
The application is designed to provide clear error messages for the most common issues. If you encounter an unhandled exception, please check the Python traceback for more details or open an issue on GitHub.

## Contributing
Contributions to the Cloud Sec Encryptor are welcome! Please fork the repository and submit a pull request with your enhancements.