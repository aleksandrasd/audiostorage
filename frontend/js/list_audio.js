function generateAudioList(groupedFiles) {
    let html = '<ul>';

    for (const [originalFileName, files] of Object.entries(groupedFiles)) {
        html += `<li>${files[0].base_name}`;
        files.forEach(file => {
            html += ` [<a href="/download/${file.file_name}/${file.new_ext_name}">${file.file_type}</a>]`;
        });
        html += '</li>';
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