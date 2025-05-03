from typing import List

from sqlalchemy import UUID, DateTime, Enum, Select, Tuple, desc, func, select

from app.audio.domain.entity.audio_file import (
    AudioFile,
    AudioFileRead,
    Policy,
    UserAudioFile,
    UserRawUploadedFile,
)
from app.audio.domain.repository.audio import AudioRepo
from app.user.domain.entity.user import User
from core.db.session import session, session_factory


class AudioSQLAlchemyRepo(AudioRepo):      
    async def get_file_extension_by_id(self, id: str) -> str:
        async with session_factory() as read_session:
            query = (
                select(AudioFile.file_type)
                .where(
                    AudioFile.id == id,
                )
            )
            result = await read_session.execute(query)
            return result.scalars().first()

    async def get_file_name_by_id(self, id: str) -> str:
        async with session_factory() as read_session:
            query = (
                select(AudioFile.file_name)
                .where(
                    AudioFile.id == id,
                )
            )
            result = await read_session.execute(query)
            return result.scalars().first()
    
    async def get_original_file_name_by_id(self, id: str) -> str | None:
        async with session_factory() as read_session:
            query = (
                select(UserRawUploadedFile.original_file_name)
                .join(UserAudioFile,
                      UserAudioFile.upload_id == UserRawUploadedFile.id)
                .where(
                    UserAudioFile.audio_file_id == id,
                )
            )
            result = await read_session.execute(query)
            return result.scalars().first()

    async def save_upload_audio_file_record(
        self, user_raw_uploaded_file: UserRawUploadedFile
    ) -> None:
        session.add(user_raw_uploaded_file)

    async def save_audio_file(self, audio_file: AudioFile) -> None:
        session.add(audio_file)

    async def save_user_audio_file(self, user_audio_file: UserAudioFile) -> None:
        session.add(user_audio_file)

    async def persist(self) -> None:
        await session.flush()

    async def get_audio_formats_for_download(self) -> List[str] | None:
        async with session_factory() as read_session:
            result = await read_session.execute(select(Policy.audio_formats_download))
            return result.scalars().first()

    async def get_audio_upload_file_max_size(self) -> int | None:
        async with session_factory() as read_session:
            result = await read_session.execute(select(Policy.upload_max_size_in_bytes))
            return result.scalars().first()

    async def get_user_upload_file_name(self, id: int, user_id: int) -> str | None:
        async with session_factory() as session:
            query = (
                select(UserRawUploadedFile.file_name)
                .join(UserAudioFile, UserAudioFile.upload_id == UserRawUploadedFile.id)
                .where(UserRawUploadedFile.id == id)
                .where(UserAudioFile.user_id == user_id)
            )
            result = await session.execute(query)
            return result.scalar()
            
    async def get_upload_file_name(self, id: int) -> str | None:
        async with session_factory() as session:
            query = (
                select(UserRawUploadedFile.file_name)
                .where(UserRawUploadedFile.id == id)
            )
            result = await session.execute(query)
            return result.scalar()

    async def download_audio_id(self, name: str) -> int:
        async with session_factory() as session:
            query = select(UserRawUploadedFile.id).where(
                UserRawUploadedFile.file_name == name
            )
            result = await session.execute(query)
            return result.scalar()
    
    async def remove_audio_file(self, audio_file_id: str) -> None:
      result = await session.execute(
          select(UserRawUploadedFile).where(UserRawUploadedFile.id == audio_file_id)
      )
      file_to_delete = result.scalar()
      await session.delete(file_to_delete)

    def _get_audio_list_query(self) -> Select:
      return (
                select(
                    UserRawUploadedFile.original_file_name,
                    User.nickname,
                    AudioFile.id.label("converted_audio_file_id"),
                    UserRawUploadedFile.id.label("audio_file_id"),
                    UserRawUploadedFile.created_at,
                    AudioFile.file_size_in_bytes,
                    AudioFile.length_in_seconds,
                    AudioFile.file_type,
                )
                .join(UserAudioFile, UserAudioFile.upload_id == UserRawUploadedFile.id)
                .join(AudioFile, UserAudioFile.audio_file_id == AudioFile.id)
                .join(User, UserAudioFile.user_id == User.id)
            )
    
    async def _get_total_count_for_audio_list(self, read_session, s):
      count_query = select(func.count()).select_from(s.subquery())
      total_count = (await read_session.execute(count_query)).scalar()
      return total_count
    
    async def _get_ordered_audio_files_records(self, read_session, s, limit, offset):
      s = (
          s
          .order_by(
              desc(UserRawUploadedFile.created_at),
              desc(AudioFile.file_type)
          )
          .limit(limit)
          .offset(offset)
      )
      result = await read_session.execute(s)
      return result.all()
        
        
    async def list_user_audio_files(
        self, nickname: str, limit: int, offset: int
    ) -> tuple[AudioFileRead, int]:
        async with session_factory() as read_session:
            s = (
                self._get_audio_list_query()
                .where(User.nickname == nickname)
            )
            total_count = await self._get_total_count_for_audio_list(read_session, s)
            audio_files = await self._get_ordered_audio_files_records(
                read_session, s, limit, offset
            )
            return audio_files, total_count

    async def list_audio_files(
        self, user_id: int | None, limit: int, offset: int
    ) -> tuple[AudioFileRead, int]:
        async with session_factory() as read_session:
            s = self._get_audio_list_query()
            if user_id:
                s = s.where(UserAudioFile.user_id == user_id)
            total_count = await self._get_total_count_for_audio_list(read_session, s)
            audio_files = await self._get_ordered_audio_files_records(
                read_session, s, limit, offset
            )
            return audio_files, total_count
  
    
    async def search_audio_files(
        self, query: str, user_id: int | None, limit: int, offset: int
    ) -> tuple[list[AudioFileRead], int]:
        async with session_factory() as read_session:
            tsquery = func.websearch_to_tsquery("simple", query)
            tsvector = func.to_tsvector(
                "simple", func.tokenize_filename(UserRawUploadedFile.original_file_name)
            )
            s = (
                self._get_audio_list_query()
                .filter(tsvector.op("@@")(tsquery))
            )
            if user_id:
                s = s.where(UserAudioFile.user_id == user_id)
            total_count = await self._get_total_count_for_audio_list(read_session, s)
            audio_files = await self._get_ordered_audio_files_records(
                read_session, s, limit, offset
            )
            return audio_files, total_count
