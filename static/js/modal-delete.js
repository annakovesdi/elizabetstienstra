// Add link to delete modal button
const deleteModal = document.getElementById('modal-delete');
deleteModal.addEventListener('show.bs.modal', event => {
    document.getElementById('delete-button').href = event.relatedTarget.getAttribute('data-bs-link');
})