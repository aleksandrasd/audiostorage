function generateAudioList(userAudioFilesPage) {
    let html = '<ul>';
	console.log(userAudioFilesPage);
    for (const userAudio of userAudioFilesPage.data) {
	  let time = new Date(userAudio.length_in_seconds * 1000).toISOString().substr(11, 8);
      html += `<li>${userAudio.base_name}`;
      userAudio.audio_types.forEach(file => {
          html += ` [<a href="/audio/${file.id}/download/${userAudio.base_name}.${file.ext}">${file.ext.toUpperCase()}</a>]`;
      });
      html += ` ${time}</li>`;
    }
    html += '</ul>';
    return html;
}
