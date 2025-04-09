function handleSearch(event) {
	if (event.key === 'Enter') {
		const query = document.getElementById('search-input').value;
		window.location.href = `/search?q=${encodeURIComponent(query)}`;
	}
}

function populateSearchFromURL() {
    const urlParams = new URLSearchParams(window.location.search);
    const query = urlParams.get('q');
    if (query) {
        const searchInput = document.getElementById('search-input');
        searchInput.value = decodeURIComponent(query);
    }
}

document.addEventListener('DOMContentLoaded', populateSearchFromURL);