document.getElementById('uploadForm').addEventListener('submit', async function(event) {
    event.preventDefault();
    const formData = new FormData(this);
    const response = await fetch('/upload', {
        method: 'POST',
        body: formData,
    });
    const result = await response.json();
    const messageDiv = document.getElementById('message');
    if (result.status === 'error') {
        messageDiv.textContent = result.message;
        messageDiv.className = 'message error';
    } else {
        messageDiv.innerHTML = `${result.message} <a href="${result.download_url}">Baixar arquivo processado</a>`;
        messageDiv.className = 'message success';
    }
    messageDiv.style.display = 'block';
});

const fileInput = document.getElementById('file');
fileInput.addEventListener('change', function () {
    // Aqui, você pode redirecionar para a nova página
    // Por exemplo:
    window.location.href = 'templates/nova-pagina.html';
});