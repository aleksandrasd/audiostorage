function generateAudioList(userAudioFiles) {
    let html = '<ul>';

    for (const userAudio of userAudioFiles) {
      html += `<li>${userAudio.base_name}`;
      userAudio.audio_types.forEach(file => {
          html += ` [<a href="/download/${file.id}/${userAudio.base_name}.${file.ext}">${file.ext.toUpperCase()}</a>]`;
      });
      html += '</li>';
    }
    html += '</ul>';
    return html;
}