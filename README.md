# Cloud Sec Encryptor

## Description
**Cloud Sec Encryptor** is a web-based Flask application that allows users to securely manage their files on Google Drive. Files are automatically encrypted before upload and decrypted after download, ensuring data security both in transit and at rest. The application provides a simple, intuitive interface for uploading and downloading files, and leverages Google Drive's API for storage operations.

## Features
- Secure file encryption before upload.
- Secure decryption of files upon download.
- User-friendly web interface for managing files on Google Drive.
- Automatic listing of all files stored in Google Drive.
- Local storage of decrypted files preserving original names and types.
- Comprehensive error handling for security and connectivity issues.

## Running the Application
To run the Cloud Sec Encryptor web application:
```bash
flask run
```
This command will start a local server, typically accessible via `http://localhost:5000`, where you can interact with the application.

## Usage

### Web Interface
- **File Listing**: Upon accessing the web application, you'll see a list of all files stored in your Google Drive.
- **Uploading Files**: Use the web form to select and upload files. Files will be encrypted automatically before the upload.
- **Downloading Files**: Click on the download link beside each file to download. Files will be decrypted automatically after the download.

## Contributing
Contributions to the Cloud Sec Encryptor are welcome! Please fork the repository and submit a pull request with your enhancements.