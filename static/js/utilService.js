import { deleteFile, downloadFile } from "./actionService.js";

// Utility function to handle API requests
export function makeApiRequest(url, method, body = null, isBlob = false) {
  // Determine headers based on whether the body is FormData
  const headers = body instanceof FormData ? {} : {"Content-Type": "application/json"};

  return fetch(url, {
    method: method,
    headers: headers,
    body: body instanceof FormData ? body : (body ? JSON.stringify(body) : null),
  })
  .then((response) => {
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    return isBlob ? response.blob() : response.json();
  })
  .catch((error) => {
    console.error("Error making the request:", error);
  });
}

// Function to format date for display
export function formatDate(dateString) {
  const options = {
    year: "numeric",
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  };
  return new Date(dateString).toLocaleDateString(undefined, options);
}

// Function to configure confirmation model
export function configureModal(fileId, actionType) {
  const modalTitle = document.getElementById("confirmationModalLabel");
  const modalBodyText = document.getElementById("modalBodyText");
  const confirmButton = document.getElementById("confirmActionButton");

  // Reset any existing event listeners
  confirmButton.replaceWith(confirmButton.cloneNode(true)); // Cloning to remove listeners
  const newConfirmButton = document.getElementById("confirmActionButton");

  // Configure the modal based on the action type
  switch (actionType) {
    case "delete":
      modalTitle.textContent = "Confirm Delete";
      modalBodyText.textContent = "Are you sure you want to delete this file?";
      newConfirmButton.classList.add("btn-danger");
      newConfirmButton.classList.remove("btn-success");
      newConfirmButton.textContent = "Delete";
      newConfirmButton.onclick = () => deleteFile(fileId);
      break;
    case "download":
      modalTitle.textContent = "Confirm Download";
      modalBodyText.textContent =
        "Are you sure you want to download this file?";
      newConfirmButton.classList.add("btn-success");
      newConfirmButton.classList.remove("btn-danger");
      newConfirmButton.textContent = "Download";
      newConfirmButton.onclick = () => downloadFile(fileId);
      break;
    case "upload":
      modalTitle.textContent = "Confirm Upload";
      modalBodyText.textContent = "Are you ready to upload this file?";
      newConfirmButton.classList.add("btn-success");
      newConfirmButton.classList.remove("btn-danger");
      newConfirmButton.textContent = "Upload";
      newConfirmButton.onclick = () => uploadFile(fileId);
      break;
  }

  // Show the modal
  const modal = new bootstrap.Modal(
    document.getElementById("confirmationModal")
  );
  modal.show();
}

// Function to show alert
export function showAlert(message, type) {
  const alertPlaceholder = document.getElementById("alertPlaceholder");
  const wrapper = document.createElement("div");
  wrapper.innerHTML = [
    `<div class="alert alert-${type} alert-dismissible fade show m-4" role="alert">`,
    `   ${message}`,
    '   <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>',
    "</div>",
  ].join("");

  alertPlaceholder.append(wrapper);
}

// Remove file row from the table
export function removeFileFromTable(fileId) {
  const row = document.querySelector(`tr[data-file-id="${fileId}"]`);
  if (row) {
    row.remove();
  }
}

// Function to show toast with autohide
export function showToast(message, type) {
  const toastContainer = document.getElementById("toastContainer");
  if (!toastContainer) {
    const container = document.createElement("div");
    container.id = "toastContainer";
    container.className = "toast-container position-fixed bottom-0 end-0 p-3";
    document.body.append(container);
  }

  const toastHTML = `
    <div class="toast align-items-center text-bg-${type} border-0" role="alert" aria-live="assertive" aria-atomic="true" data-bs-autohide="true" data-bs-delay="5000">
      <div class="d-flex">
        <div class="toast-body">
          ${message}
        </div>
        <button type="button" class="btn-close me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
      </div>
    </div>
  `;

  const toastWrapper = document.createElement("div");
  toastWrapper.innerHTML = toastHTML;
  const toastElement = toastWrapper.firstChild;

  document.getElementById("toastContainer").append(toastElement);

  const toast = new bootstrap.Toast(toastElement);
  toast.show();
}
