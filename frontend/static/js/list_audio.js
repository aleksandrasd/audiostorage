function generateAudioList(userAudioFilesPage, add_remove_link = false, add_nickname_link = false) {
    let html = '<ul>';
	console.log(userAudioFilesPage);
    for (const userAudio of userAudioFilesPage.data) {
	  let time = new Date(userAudio.length_in_seconds * 1000).toISOString().substr(11, 8);
      html += `<li>${userAudio.base_name}`;
	  if (add_remove_link) {
	    html += ` <a href="#" onclick="event.preventDefault(); fetch('/api/v1/audio/${userAudio.upload_file_name_id}/remove', {method: 'POST'}).then(() => window.location.reload())">Remove</a>&emsp;`
	  }
      userAudio.audio_types.forEach(file => {
          html += ` [<a href="/api/v1/audio/${file.id}/download/${userAudio.base_name}.${file.ext}">${file.ext.toUpperCase()}</a>]`;
      });
      html += ` ${time}`;
	  if (add_nickname_link){
		html += ` &emsp; (<a href="/user?nickname=${userAudio.nickname}">${userAudio.nickname}</a>)`;  
	  }
	  html += `</li>`;
    }
    html += '</ul>';
    return html;
}
