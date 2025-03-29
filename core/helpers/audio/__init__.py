
from collections import defaultdict
import os
from app.audio.adapter.input.api.v1.response import AudioFilesPaginationResponse
from app.audio.domain.entity.audio_file import AudioFileCountedRead, AudioFileRead


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
    
    @classmethod
    def create_audio_files_pagination_response(cls, audio_files_counted: AudioFileCountedRead):
      return  AudioFilesPaginationResponse.create(
        data = AudioHelper.format_file_list(audio_files_counted.audio_files),
        offset=audio_files_counted.offset,
        limit=audio_files_counted.limit,
        total_records=audio_files_counted.total_records
    ) 