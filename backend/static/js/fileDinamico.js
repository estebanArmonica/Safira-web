document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('archivo');
    const filePreview = document.getElementById('file-preview');
    const fileName = document.getElementById('selected-file-name');
    const fileSize = document.getElementById('selected-file-size');
    const removeBtn = document.getElementById('remove-file');

    fileInput.addEventListener('change', function(e) {
        if (e.target.files.length > 0) {
            const file = e.target.files[0];
            fileName.textContent = file.name;
            fileSize.textContent = formatFileSize(file.size);
            filePreview.style.display = 'flex';
        }
    });

    removeBtn.addEventListener('click', function() {
        fileInput.value = '';
        filePreview.style.display = 'none';
    });

    function formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
});