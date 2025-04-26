// Boolean flag to prevent double uploads during a single interaction
let isUploading = false;

// Get references to important DOM elements
const dropArea = document.getElementById('drop-area');
const fileInput = document.getElementById('fileInput');
const browseButton = document.getElementById('browseButton');
const uploadUrlInput = document.getElementById('uploadUrl');
const copyButton = document.getElementById('copyButton');
const showGalleryButton = document.getElementById('btnGoToImages');

//Event listener to Show Gallery click
showGalleryButton.addEventListener('click', () => {
    window.location.href = '/images/';
});


// Add event listener to 'Browse Your File' button
browseButton.addEventListener('click', () => {
    fileInput.click(); // Open the file dialog
});

// Prevent default behavior for drag-and-drop events
["dragenter", "dragover", "dragleave", "drop"].forEach(eventName => {
    dropArea.addEventListener(eventName, preventDefaults);
});

function preventDefaults(event) {
    event.preventDefault();
    event.stopPropagation();
}

// Highlight the upload area when a file is dragged over it
dropArea.addEventListener('dragover', () => dropArea.classList.add('dragover'));

// Remove the highlight when the drag leaves the upload area
dropArea.addEventListener('dragleave', () => dropArea.classList.remove('dragover'));

// Handle dropping files into the upload area
dropArea.addEventListener('drop', (event) => {
    dropArea.classList.remove('dragover');
    const files = event.dataTransfer?.files;

    // Ensure files are present before processing
    if (files?.length > 0) {
        handleDropFiles(files); // Handles and uploads files
    }
});

// Handle the file input `change` event
fileInput.addEventListener('change', () => {
    const files = fileInput.files;

    // Ensure files are present before processing
    if (files.length > 0) {
        handleInputFiles(files);
    }
});

/**
 * Handle dropped files without interfering with the file input
 */
function handleDropFiles(files) {
    if (isUploading) return;
    const file = files[0];
    if (!file) return;

    // Validate and upload the file directly
    const isValid = validateFile(file);
    if (isValid) {
        uploadFile(file);
    }
}

/**
 * Handle files selected via the file input dialog
 */
function handleInputFiles(files) {
    if (isUploading) return;
    const file = files[0];
    if (!file) return;

    // Validate and upload the file directly
    const isValid = validateFile(file);
    if (isValid) {
        uploadFile(file);
    }
}

/**
 * Validate the file
 * @param {File} file - The file object to validate
 * @returns {boolean} - Whether the file is valid
 */
function validateFile(file) {
    // Validate file type
    if (!['image/jpeg', 'image/png', 'image/gif'].includes(file.type)) {
        dropArea.classList.add('error');
        alert('Invalid file type. Only JPEG, PNG, and GIF are allowed.');
        return false;
    }

    // Validate file size
    const maxFileSize = 5 * 1024 * 1024; // 5 MB
    if (file.size > maxFileSize) {
        dropArea.classList.add('error');
        alert('File size exceeds the 5 MB limit.');
        return false;
    }

    // If validation passed, clear errors
    dropArea.classList.remove('error');
    return true;
}

/**
 * Upload the file to the server
 * @param {File} file - The file to upload
 */
function uploadFile(file) {
    // Prevent duplicate uploads
    if (isUploading) return;

    // Set flag to indicate an upload is in progress
    isUploading = true;
    dropArea.classList.add('uploading');

    fetch('/api/upload/', {
        method: 'POST',
        headers: {
            'Filename': file.name
        },
        body: file
    })
            .then(response => {
                if (!response.ok) throw new Error('Upload failed');
                return response.headers.get('Location');
            })
            .then(location => {
                // On success, show the success popup
                showPopup('File uploaded successfully!', true);

                // Update the UI with the uploaded file URL
                uploadUrlInput.value = location;
                copyButton.disabled = false;
            })
            .catch(error => {
                console.error(error);

                // On error, show the failure popup
                showPopup('Upload failed. Please try again.', false);
            })
            .finally(() => {
                // Reset uploading state
                isUploading = false;
                dropArea.classList.remove('uploading');
            });
}

/**
 * Display a popup notification
 * @param {string} message - The message to display
 * @param {boolean} isSuccess - Whether the message indicates success (green) or failure (red)
 */
function showPopup(message, isSuccess) {
    const popup = document.getElementById('uploadResultPopup');
    popup.textContent = message;
    popup.classList.remove('hidden', 'success', 'error');
    popup.classList.add('visible', isSuccess ? 'success' : 'error');

    // Hide popup after 2 seconds
    setTimeout(() => {
        popup.classList.remove('visible');
        popup.classList.add('hidden');
    }, 2000);
}

// Event listener to copy URL to clipboard
copyButton.addEventListener('click', () => {
    const uploadUrl = uploadUrlInput.value;
    if (!uploadUrl) {
        alert('No URL available to copy.');
        return;
    }

    navigator.clipboard.writeText(uploadUrl)
            .then(() => alert('URL copied to clipboard!'))
            .catch(err => console.error('Failed to copy URL:', err));
});