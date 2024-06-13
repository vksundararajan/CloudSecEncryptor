// Utility function to handle API requests
function makeApiRequest(url, method, body = null) {
  return fetch(url, {
    method: method,
    headers: {
      'Content-Type': 'application/json',
    },
    body: body ? JSON.stringify(body) : null,
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      return response.json();
    })
    .catch((error) => {
      console.error('Error making the request:', error);
    });
}

// Fetch list of files from the server
function fetchFiles() {
  makeApiRequest('/api/files', 'GET').then((files) => {
    const fileListElement = document.querySelector('.file-list');
    fileListElement.innerHTML = ''; // Clear existing list

    if (files) {
      files.forEach((file) => {
        const listItem = document.createElement('li');
        listItem.innerHTML = `<i class='fas'></i> ${file.name}`;
        fileListElement.appendChild(listItem);
      });
    } else {
      fileListElement.innerHTML = `<li class="empty">No files available.</li>`;
    }
  });
}

// Download a file specified by fileName
function downloadFile(fileName) {
  makeApiRequest(`/api/download/${fileName}`, 'POST').then((response) => {
    console.log('Download successful:', response);
    alert('File downloaded successfully!');
  });
}

// Handle file upload event
function uploadFiles() {
  const fileInput = document.querySelector(`input[type='file']`);
  const files = fileInput.files;
  if (files.length === 0) {
    alert('Please select a file to upload.');
    return;
  }
  const formData = new FormData();
  for (const file of files) {
    formData.append('files', file);
  }

  fetch('/api/upload', {
    method: 'POST',
    body: formData,
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      return response.json();
    })
    .then((result) => {
      console.log('Upload successful:', result);
      alert('File uploaded successfully!');
      fetchFiles(); // Refresh file list
    })
    .catch((error) => {
      console.error('Error uploading files:', error);
    });
}

// Event listeners for upload button
document.addEventListener('DOMContentLoaded', function () {
  fetchFiles();

  const uploadButton = document.querySelector('.upload-btn');
  uploadButton.addEventListener('click', () => {
    document.querySelector(`input[type='file']`).click(); // Simulate file input click
  });

  // Optionally, automatically fetch files when the document is ready
  fetchBufferedFiles();
});
