function renderPagination({ endpoint, current_page, next_page, prev_page, total_pages, total_records }) {
  const container = document.getElementById('pagination');
  if (!container) {
    console.error('Pagination container not found');
    return;
  }

  container.innerHTML = '';

  const info = document.createElement('div');
  info.textContent = `Page ${current_page} of ${total_pages} (${total_records} records)`;
  container.appendChild(info);

  const nav = document.createElement('div');
  nav.classList.add('pagination-controls');
	
  const prevBtn = document.createElement('button');
  prevBtn.textContent = 'Previous';
  prevBtn.disabled = prev_page === null;
  if (prev_page !== null) {
    prevBtn.onclick = () => {
	  const params = endpoint.searchParams;
	  params.append('page', prev_page);
      window.location.href = urlObj.pathname + urlObj.search;
    };
  }
  nav.appendChild(prevBtn);

  const currentSpan = document.createElement('span');
  currentSpan.textContent = ` ${current_page} `;
  nav.appendChild(currentSpan);

  const nextBtn = document.createElement('button');
  nextBtn.textContent = 'Next';
  nextBtn.disabled = next_page === null;
  if (next_page !== null) {
    nextBtn.onclick = () => {
	  const params = endpoint.searchParams;
	  params.append('page', next_page);
      window.location.href = urlObj.pathname + urlObj.search
    };
  }
  nav.appendChild(nextBtn);

  container.appendChild(nav);
}