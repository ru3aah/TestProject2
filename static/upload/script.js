const dropArea = document.getElementById('drop-area');
const fileInput = document.getElementById('fileInput');
const browseButton = document.getElementById('browseButton');
const uploadUrlInput = document.getElementById('uploadUrl');
const copyButton = document.getElementById('copyButton');

// Popup notification function for messaging
function showPopupNotification(message, type) {
    const notification = document.createElement('div');
    notification.className = `popup-notification ${type}`;
    notification.textContent = message;
    document.body.appendChild(notification);

    setTimeout(() => {
        document.body.removeChild(notification);
    }, 3000); // The popup disappears after 3 seconds
}

// Validate file type and size
function validateFile(file) {
    const allowedTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/jpg'];
    const maxSize = 5 * 1024 * 1024; // 5MB

    if (!allowedTypes.includes(file.type)) {
        showPopupNotification('Unsupported file type. Only JPG, PNG, and GIF are allowed.', 'error');
        return 'type';
    }

    if (file.size > maxSize) {
        showPopupNotification('File size exceeds 5MB!', 'error');
        return 'size';
    }

    return 'valid';
}

// Handle dropped or selected files
function handleFiles(files) {
    const file = files[0];
    if (!file) return;

    const validationResult = validateFile(file);

    if (validationResult === 'type' || validationResult === 'size') {
        dropArea.classList.add('error');
        dropArea.classList.remove('success');
        return;
    }

    dropArea.classList.remove('error');
    dropArea.classList.add('success');

    // file upload
    uploadFile(file);
}

// file upload via API with error handling
async function uploadFile(file) {
    try {
        const response = await fetch('/api/upload/', {
            method: 'POST',
            headers: {
                'Filename': file.name
            },
            body: file
        });

        if (!response.ok) {
            throw new Error('Failed to upload file.');
        }

        const uploadUrl = response.headers.get('Location');
        uploadUrlInput.value = uploadUrl;

        copyButton.disabled = false;

        showPopupNotification('File uploaded successfully!', 'success');
    } catch (error) {
        console.error('Upload error:', error);
        dropArea.classList.remove('success');
        dropArea.classList.add('error');
        showPopupNotification('Error uploading file. Please try again.', 'error');
    }
}

// Add Drag-and-Drop functionality
browseButton.addEventListener('click', () => {
    fileInput.click();
});

fileInput.addEventListener('change', () => {
    handleFiles(fileInput.files);
});

dropArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropArea.classList.add('dragover');
});

dropArea.addEventListener('dragleave', () => {
    dropArea.classList.remove('dragover');
});

dropArea.addEventListener('drop', (e) => {
    e.preventDefault();
    dropArea.classList.remove('dragover');
    const files = e.dataTransfer.files;
    if (files.length) {
        handleFiles(files);
    }
});

// Copying upload URL to clipboard
copyButton.addEventListener('click', () => {
    navigator.clipboard.writeText(uploadUrlInput.value)
            .then(() => {
                copyButton.textContent = 'Copied!';
                copyButton.style.backgroundColor = '#7B7B7B';
                setTimeout(() => {
                    copyButton.innerHTML = '<img src="copy.png" alt="Copy" width="20" height="20">';
                    copyButton.style.backgroundColor = '#007BFF';
                    uploadUrlInput.value = '';
                }, 1000);
            })
            .catch((err) => {
                console.error('Failed to copy:', err);
                showPopupNotification('Failed to copy upload URL.', 'error');
            });
});

//Go to images list button
document.getElementById('btnGoToImages').addEventListener('click', (event) => {
    window.location.href = '/images/';
});