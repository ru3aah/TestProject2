const dropArea = document.getElementById('drop-area');
const fileInput = document.getElementById('fileInput');
const browseButton = document.getElementById('browseButton');
const uploadUrlInput = document.getElementById('uploadUrl');
const copyButton = document.getElementById('copyButton');

browseButton.addEventListener('click', () => {
  fileInput.click();
});

// Handle drag-enter and drag-leave for visual feedback
dropArea.addEventListener('dragover', (e) => {
  e.preventDefault();
  dropArea.classList.add('dragover');
});

dropArea.addEventListener('dragleave', () => {
  dropArea.classList.remove('dragover');
});

// Handle the drop event
dropArea.addEventListener('drop', (e) => {
  e.preventDefault();
  dropArea.classList.remove('dragover');
  const files = e.dataTransfer.files;
  if (files.length) {
    handleFiles(files);
  }
});

// When file input changes (file selection)
fileInput.addEventListener('change', () => {
  handleFiles(fileInput.files);
});

// Main function to handle files
function handleFiles(files) {
  const file = files[0];
  if (!file) return;

  // Validate file type
  if (!['image/jpeg', 'image/png', 'image/gif', 'image/jpg'].includes(file.type)) {
    showFeedback('Invalid file type. Please upload a valid image file.', 'error');
    return;
  }

  // Validate file size (limit: 5 MB)
  if (file.size > 5 * 1024 * 1024) {
    showFeedback('File size exceeds 5MB limit. Please upload a smaller image.', 'error');
    return;
  }

  // Clear all errors and upload file
  uploadFile(file);
}

// Function to upload file
function uploadFile(file) {
  fetch('/api/upload/', {
    method: 'POST',
    headers: {
      'Filename': file.name
    },
    body: file,
  })
    .then(response => {
      if (!response.ok) {
        showFeedback('Failed to upload file. Please try again.', 'error');
        throw new Error('Upload failed');
      }

      // Extract the upload location URL from response
      const uploadUrl = response.headers.get('Location');
      if (uploadUrl) {
        uploadUrlInput.value = uploadUrl;
        copyButton.disabled = false;
        showFeedback('File uploaded successfully!', 'success');
      } else {
        throw new Error('No URL returned in response.');
      }
    })
    .catch(error => {
      console.error('Upload error:', error);
      showFeedback('An error occurred during the upload. Please try again.', 'error');
    });
}

// Function to display feedback (success or error)
function showFeedback(message, type) {
  dropArea.classList.remove('error', 'success');

  if (type === 'error') {
    dropArea.classList.add('error');
  } else if (type === 'success') {
    dropArea.classList.add('success');
  }

  const feedbackElement = document.getElementById('feedback');
  feedbackElement.textContent = message;
  feedbackElement.className = type;

  // Clear feedback after 3 seconds
  setTimeout(() => {
    feedbackElement.textContent = '';
    feedbackElement.className = '';
  }, 3000);
}

// Copy button functionality
copyButton.addEventListener('click', () => {
  navigator.clipboard
    .writeText(uploadUrlInput.value)
    .then(() => {
      copyButton.textContent = 'Copied!';
      copyButton.style.backgroundColor = '#7B7B7B';
      setTimeout(() => {
        copyButton.innerHTML =
          '<img src="copy.png" alt="Copy" width="20" height="20">';
        copyButton.style.backgroundColor = '#007BFF';
      }, 1000);
    })
    .catch(err => {
      console.error('Failed to copy:', err);
    });
});

// Redirect button functionality
document.getElementById('btnGoToImages').addEventListener('click', () => {
  window.location.href = '/images/';
});