function addHeaderContent() {
    // Create the HTML string
    const htmlString = `
    <div class="nav-links">
        <a href="/list_user_audio">My Files</a>
        <label for="file-upload" style="cursor: pointer;">Upload</label>
        <div class="search-box">
        </div>
            <input type="text" id="search-input" placeholder="Search..." onkeypress="handleSearch(event)">
    </div>
    <input type="file" id="file-upload" class="upload-input" accept="audio/*,video/*" onchange="handleFileUpload()">
    `;

    const header = document.querySelector('header');
	header.innerHTML = htmlString;
}

addHeaderContent();