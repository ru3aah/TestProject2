const dropArea = document.getElementById('drop-area');
const fileInput = document.getElementById('fileInput');
const browseButton = document.getElementById('browseButton');
const uploadUrlInput = document.getElementById('uploadUrl');
const copyButton = document.getElementById('copyButton');

browseButton.addEventListener('click', () => {
  fileInput.click();
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

fileInput.addEventListener('change', () => {
  handleFiles(fileInput.files);
});

function handleFiles(files) {
  const file = files[0];
  if (!file) return;

  if (!['image/jpeg','image/png','image/gif', 'image/jpg'].includes(file.type)) {
    // Error
    dropArea.classList.add('error');
    dropArea.classList.remove('success');
    return;
  }

  if (file.size > 5 * 1024 * 1024) {
    dropArea.classList.add('error');
    dropArea.classList.remove('success');
    return;
  }

  dropArea.classList.remove('error');


}


copyButton.addEventListener('click', () => {
  navigator.clipboard.writeText(uploadUrlInput.value)
    .then(() => {
      copyButton.textContent = 'Copied!';
      copyButton.style.backgroundColor = '#7B7B7B';
      setTimeout(() => {
        copyButton.innerHTML = '<img src="copy.png" alt="Copy" width="20" height="20">';
        copyButton.style.backgroundColor = '#007BFF';
      }, 1000);
    })
    .catch((err) => {
      console.error('Failed to copy:', err);
    });
});

fileInput.addEventListener('change', () => {
  const file = fileInput.files[0];
  if (!file) return alert('Pick up a file to upload');

  fetch('/api/upload/', {
    method: 'POST',
    headers: {
      'Filename': file.name
    },
    body: file
  })
  .then(response => {
    document.getElementById('uploadUrl').value = response.headers.get('Location');

    copyButton.disabled = false;
    dropArea.classList.add('success');
  })
  .catch(error => {
    console.error('Upload error:', error);
    dropArea.classList.add('error');
  });
});

document.getElementById('btnGoToImages').addEventListener('click', (event) => {
    window.location.href = '/images/';
});