// Add link to delete modal button
const deleteModal = document.getElementById('modal-delete');
deleteModal.addEventListener('show.bs.modal', event => {
    console.log("in the loop!");
    var button = event.relatedTarget;
    var link = button.getAttribute('data-bs-link');
    var a = document.getElementById('delete-button');
    a.href = link;
    console.log(link + a.href);
})