function handleSearch(event) {
	if (event.key === 'Enter') {
		const query = document.getElementById('search-input').value;
		window.location.href = `/search?q=${encodeURIComponent(query)}`;
	}
}

function get_search_query(){
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('q');	
}

function populateSearchFromURL() {
	query = get_search_query();
    if (query) {
        const searchInput = document.getElementById('search-input');
        searchInput.value = decodeURIComponent(query);
    }
}

document.addEventListener('DOMContentLoaded', populateSearchFromURL);