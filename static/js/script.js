import {
  uploadFiles,
  fetchBufferedFiles
} from "./actionService.js";
import { configureModal } from './utilService.js';

// Function to handle the initialization of page data
function initializePage() {
  // DOMContentLoaded event listener
  document.addEventListener("DOMContentLoaded", async () => {
    await fetchBufferedFiles();

    const actionButtons = document.querySelectorAll('button[data-action]');
    const uploadBtn = document.getElementById("uploadBtn");

    if (actionButtons) {
      actionButtons.forEach(button => {
        button.addEventListener("click", (event) => {
          const fileId = button.getAttribute('data-file-id');
          const actionType = button.getAttribute('data-action');
          configureModal(fileId, actionType);
        });
      });
    }

    if (uploadBtn) {
      uploadBtn.addEventListener("click", () => {
        uploadFiles();
      });
    }
  });
}

initializePage();