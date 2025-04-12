function handleFileUpload() {
	const fileInput = document.getElementById('file-upload');
	const file = fileInput.files[0];
	if (file) {
		const formData = new FormData();
		formData.append('file', file);
		fetch('/upload', {
			method: 'POST',
			body: formData,
		})
		.then(response => response.json())
		.then(data => {
			console.log('File uploaded:', data);
			const taskId = data.task_id;
			window.location.href = '/list_user_audio'
		})
		.catch(error => {
			console.error('Error uploading file:', error);
			alert('Error uploading file.');
		});
	}
}