document.getElementById('uploadBtn').addEventListener('click', () => {
    const csvFile = document.getElementById('csvFile').files[0];
    const txtFile = document.getElementById('txtFile').files[0];

    if (!csvFile || !txtFile) {
        alert('Please select both files.');
        return;
    }

    const formData = new FormData();
    formData.append('csvFile', csvFile);
    formData.append('txtFile', txtFile);

    fetch('https://your-lambda-url.amazonaws.com/your-endpoint', {
        method: 'POST',
        body: formData
    })
        .then(response => response.blob())
        .then(blob => {
            const url = URL.createObjectURL(blob);
            chrome.downloads.download({
                url: url,
                filename: 'result.xlsx',
                saveAs: true
            });
        })
        .catch(error => console.error('Error:', error));
});
