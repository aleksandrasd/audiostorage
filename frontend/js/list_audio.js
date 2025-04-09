function generateAudioList(groupedFiles) {
    let html = '<ul>';
    let time = new Date(userAudioFiles.length_in_seconds * 1000).toISOString().substr(11, 8);
    for (const userAudio of userAudioFiles) {
      html += `<li>${userAudio.base_name}`;
      userAudio.audio_types.forEach(file => {
          html += ` [<a href="/download/${file.id}/${userAudio.base_name}.${file.ext}">${file.ext.toUpperCase()}</a>]`;
      });
      html += ` ${time}</li>`;
    }
    html += '</ul>';
    return html;
}

/* const list_user_audio = {
    "file1.wav": [
        { "base_name": "file1", "file_name": "file1.wav", "new_ext_name": "file1.mp3", "file_type": "MP3" },
        { "base_name": "file1", "file_name": "file1.wav", "new_ext_name": "file1.ogg", "file_type": "OGG" }
    ],
    "file2.wav": [
        { "base_name": "file2", "file_name": "file2.wav", "new_ext_name": "file2.mp3", "file_type": "MP3" }
    ]
};

const generatedHTML = generateAudioList(list_user_audio);
console.log(generatedHTML); */