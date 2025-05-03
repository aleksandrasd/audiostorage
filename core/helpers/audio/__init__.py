
from collections import defaultdict
import os
from app.audio.adapter.input.api.v1.response import AudioFile, AudioFilesPaginationResponse, AudioType
from app.audio.domain.entity.audio_file import  AudioFileCountedRead, AudioFileRead
from core.utils import extract_base_name


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
    
    def get_audio_file_objects(audio_files: list[AudioFileRead]) -> list[AudioFile]:
      files_by_base_name = {}
      
      for file in audio_files:
          base_name = extract_base_name(file.original_file_name)
          
          if file.audio_file_id not in files_by_base_name:
              files_by_base_name[file.audio_file_id] = {
                  'base_name': base_name,
                  'nickname': file.nickname,
                  'length_in_seconds': file.length_in_seconds,
                  'upload_file_name_id': file.audio_file_id,
                  'audio_types': []
              }
          
          audio_type = AudioType(
              id=file.converted_audio_file_id,
              ext=file.file_type.lower(),
              file_type=file.file_type.upper(),
              file_size_in_bytes=file.file_size_in_bytes 
          )
          
          files_by_base_name[file.audio_file_id]['audio_types'].append(audio_type)
      
      return [AudioFile(**file_data) for file_data in files_by_base_name.values()]
      

    @classmethod
    def create_audio_files_pagination_response(cls, audio_files_counted: AudioFileCountedRead):
      return  AudioFilesPaginationResponse.create(
        data = cls.get_audio_file_objects(audio_files_counted.data),
        offset=audio_files_counted.offset,
        limit=audio_files_counted.limit,
        total_records=audio_files_counted.total_records
    ) 