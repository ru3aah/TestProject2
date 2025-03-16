const tbody = document.getElementById('imagesTableBody');

// Fetch and render images
fetch('/api/images')
        .then(response => response.json())
        .then(images => setImages(images.images))
        .catch(err => {
            console.error('Failed to retrieve images:', err);
            showPopupNotification('Failed to load images.', 'error');
        });

function setImages(images) {
    images.forEach(image => {
        const tr = document.createElement('tr');

        const tdPreview = document.createElement('td');
        const tdUrl = document.createElement('td');
        const tdDelete = document.createElement('td');

        const deleteButton = document.createElement('button');
        deleteButton.classList.add('delete-btn');
        deleteButton.textContent = 'X';
        deleteButton.addEventListener('click', () => confirmAndDeleteImage(image, tr));

        tdDelete.appendChild(deleteButton);
        tdPreview.innerHTML = `<img src="/images/${image}" width="43" height="100%">`;
        tdUrl.innerHTML = `<a href="/images/${image}" target="_blank">${image}</a>`;

        tr.appendChild(tdPreview);
        tr.appendChild(tdUrl);
        tr.appendChild(tdDelete);

        tbody.appendChild(tr);
    });
}

// Function to show confirmation dialog and delete image
function confirmAndDeleteImage(image, tableRow) {
    const confirmation = showConfirmationDialog(
            `Are you sure you want to delete the image: ${image}?`
    );

    confirmation.then(confirmed => {
        if (confirmed) {
            deleteImage(image, tableRow);
        }
    });
}

// Perform API request to delete the image
function deleteImage(image, tableRow) {
    fetch(`/api/images/${image}`, {
        method: 'DELETE'
    })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to delete image.');
                }

                // Remove the table row after successful deletion
                tableRow.remove();
                showPopupNotification('Image deleted successfully.', 'success');
            })
            .catch(err => {
                console.error('Deletion error:', err);
                showPopupNotification('Failed to delete image. Please try again.', 'error');
            });
}

// Show confirmation dialog
function showConfirmationDialog(message) {
    return new Promise(resolve => {
        const dialogBackdrop = document.createElement('div');
        dialogBackdrop.className = 'dialog-backdrop';

        const dialogBox = document.createElement('div');
        dialogBox.className = 'dialog-box';

        const dialogMessage = document.createElement('p');
        dialogMessage.textContent = message;

        const btnConfirm = document.createElement('button');
        btnConfirm.textContent = 'Yes';
        btnConfirm.className = 'dialog-btn confirm';
        btnConfirm.addEventListener('click', () => {
            resolve(true);
            cleanupDialog();
        });

        const btnCancel = document.createElement('button');
        btnCancel.textContent = 'No';
        btnCancel.className = 'dialog-btn cancel';
        btnCancel.addEventListener('click', () => {
            resolve(false);
            cleanupDialog();
        });

        dialogBox.appendChild(dialogMessage);
        dialogBox.appendChild(btnConfirm);
        dialogBox.appendChild(btnCancel);

        dialogBackdrop.appendChild(dialogBox);
        document.body.appendChild(dialogBackdrop);

        function cleanupDialog() {
            document.body.removeChild(dialogBackdrop);
        }
    });
}

// Popup notification for user feedback
function showPopupNotification(message, type) {
    const notification = document.createElement('div');
    notification.className = `popup-notification ${type}`;
    notification.textContent = message;

    document.body.appendChild(notification);

    setTimeout(() => {
        document.body.removeChild(notification);
    }, 3000); // Fades out after 3 seconds
}

document.getElementById('btnGoToUpload').addEventListener('click', () => {
    window.location.href = '/upload/';
});