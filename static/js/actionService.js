import {
  makeApiRequest,
  removeFileFromTable,
  showToast,
  formatDate,
} from "./utilService.js";

// Delete a file specified by fileId
export function deleteFile(fileId) {
  makeApiRequest(`/delete/${fileId}`, "POST").then(response => {
    const deleteModal = bootstrap.Modal.getInstance(document.getElementById('confirmationModal'));
    deleteModal.hide(); // Hide the modal regardless of the response outcome

    if (response.message) {
      showToast('File deleted successfully', 'success');
      removeFileFromTable(fileId);
    } else {
      showToast('Failed to delete the file', 'danger');
    }
  }).catch(error => {
    console.error('Error:', error);
    showToast('Error deleting file', 'danger');
  });
}

// Download a file specified by fileId
export function downloadFile(fileId) {
  makeApiRequest(`/download/${fileId}`, "GET", null, true).then(blob => {
    // Create a URL for the blob object
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = "downloaded_file";  // Optionally set a filename here
    document.body.appendChild(a);
    a.style.display = 'none';  // Hide the anchor element
    a.click();  // Simulate a click to download
    a.remove();  // Clean up the DOM
    window.URL.revokeObjectURL(url);  // Free up resources by revoking the blob URL
  }).catch(error => {
    console.error('Error:', error);
    showToast('Error downloading file', 'danger');
  });
}

// Function to fetch files from the cloud and update the UI
export async function fetchBufferedFiles() {
  try {
    let files = await makeApiRequest("/api/files", "GET");
    files = files.files;
    if (!Array.isArray(files)) {
      throw new Error("Expected an array of files, but got: " + typeof files);
    }

    const fileListElement = document.getElementById("fileList");
    if (!fileListElement) {
      throw new Error("The fileList element does not exist in the DOM");
    }

    fileListElement.innerHTML = "";  // Clear existing content

    files.forEach((file, index) => {
      const row = `<tr data-file-id="${file.fileId}">
        <th scope="row">${index + 1}</th>
        <td>${file.fileName}</td>
        <td>${file.size}</td>
        <td>${formatDate(file.lastModified)}</td>
        <td>
        <button class="btn btn-success btn-sm" data-action="download" data-file-id="${file.fileId}"><i class="fas fa-trash-alt"></i> Download</button>
          <button class="btn btn-danger btn-sm" data-action="delete" data-file-id="${file.fileId}"><i class="fas fa-trash-alt"></i> Delete</button>
        </td>
      </tr>`;
      fileListElement.innerHTML += row;
    });
  } catch (error) {
    console.error("Error fetching files:", error);
    showToast(error.message, 'danger');
  }
}

// Handle file upload event
export function uploadFiles() {
  const files = document.getElementById('fileInput').files;
  const formData = new FormData();
  
  for (let i = 0; i < files.length; i++) {
    formData.append('files', files[i]);
  }

  makeApiRequest('/api/upload', 'POST', formData)
    .then(data => {
      console.log(data);  // Log or handle the response data
      showToast('Files uploaded successfully!', 'success');
    })
    .catch(error => {
      console.error('Error uploading files:', error);
      showToast('Error uploading files', 'danger');
    });
}
