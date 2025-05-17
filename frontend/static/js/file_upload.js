  

function handleFileUpload() {
    const fileInput = document.getElementById('file-upload');
    const file = fileInput.files[0];
    if (file) {
        const formData = new FormData();
        formData.append('file', file);
        fetchData('/api/v1/audio/upload', {
            method: 'POST',
            body: formData,
        })
        .then(response => {
            if (response.status === 401) {
                window.location.href = '/login';
                return;
            }
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
			console.log(response);
            return response.json();
        })
        .then(data => {
            if (data) {  
                console.log('File uploaded:', data);
                const taskId = data.task_id;
				console.log(data);
            }
        })
        .catch(error => {
            console.error('Error uploading file:', error);
            alert('Error uploading file: ' + error.message);
        });
    }
}