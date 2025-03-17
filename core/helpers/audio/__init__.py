
from collections import defaultdict
import os
from app.audio.domain.entity.audio_file import AudioFileRead


class AudioHelper:
    
    @staticmethod
    def format_file_list(audio_files: list[AudioFileRead]):  
      grouped_files = defaultdict(list)
      for file in audio_files:
          audio = file.model_dump()
          base_name = os.path.splitext(audio['original_file_name'])[0]  
          audio['base_name'] = base_name
          audio['new_ext_name'] =  f"{base_name}.{audio['file_type']}"
          grouped_files[str(file.created_at)].append(audio)

      return grouped_files