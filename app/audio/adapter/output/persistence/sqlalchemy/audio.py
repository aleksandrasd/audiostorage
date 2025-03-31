from typing import List

from sqlalchemy import desc, func, select

from app.audio.domain.entity.audio_file import (
    AudioFile,
    AudioFileCountedRead,
    AudioFileRead,
    Policy,
    UserAudioFile,
    UserRawUploadedFile,
)
from app.audio.domain.repository.audio import AudioRepo
from app.user.domain.entity.user import User
from core.db.session import session, session_factory


class AudioSQLAlchemyRepo(AudioRepo):      
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
                .join(UserRawUploadedFile,
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


    async def get_raw_file_name(self, id: int) -> str:
        async with session_factory() as session:
            query = select(UserRawUploadedFile.file_name).where(
                UserRawUploadedFile.id == id
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

    async def get_file_type_by_filenames(
        filename: str, original_file_name: str
    ) -> str | None:
        async with session_factory() as read_session:
            query = (
                select(AudioFile.file_type)
                .join(UserAudioFile, AudioFile.id == UserAudioFile.audio_file_id)
                .join(
                    UserRawUploadedFile,
                    UserAudioFile.upload_id == UserRawUploadedFile.id,
                )
                .where(
                    UserAudioFile.audio_file_id == AudioFile.id,
                    UserRawUploadedFile.original_file_name == original_file_name,
                    AudioFile.file_name == filename,
                )
            )
            result = await read_session.execute(query)
            return result.scalars().first()

    async def list_audio_files(
        self, user_id: int | None, limit: int, offset: int
    ) -> tuple[AudioFileRead, int]:
        async with session_factory() as read_session:
            s = (
                select(
                    UserAudioFile.user_id,
                    UserRawUploadedFile.original_file_name,
                    AudioFile.file_name,
                    UserRawUploadedFile.created_at,
                    AudioFile.file_size_in_bytes,
                    AudioFile.length_in_seconds,
                    User.nickname,
                    AudioFile.file_type,
                )
                .join(UserAudioFile, UserAudioFile.upload_id == UserRawUploadedFile.id)
                .join(AudioFile, UserAudioFile.audio_file_id == AudioFile.id)
                .join(User, UserAudioFile.user_id == User.id)
            )
            if user_id:
                s = s.where(UserAudioFile.user_id == user_id)
            total_count = s.count()
            s = (
                s
                .order_by(desc(UserRawUploadedFile.created_at).desc(AudioFile.file_type))
                .limit(limit)
                .offset(offset)
            )
            result = await read_session.execute(s)
            return result.all(), total_count

    async def files_full_text_search(
        self, query: str, user_id: int | None, limit: int, offset: int
    ) -> AudioFileCountedRead:
        async with session_factory() as read_session:
            # Construct the full-text search condition
            tsquery = func.websearch_to_tsquery("simple", query)
            tsvector = func.to_tsvector(
                "simple", func.tokenize_filename(UserRawUploadedFile.original_file_name)
            )

            # Build the query with the full-text search condition
            query = (
                select(
                    UserAudioFile.user_id,
                    UserRawUploadedFile.original_file_name,
                    UserRawUploadedFile.file_name,
                    UserRawUploadedFile.created_at,
                    AudioFile.file_size_in_bytes,
                    AudioFile.length_in_seconds,
                    User.nickname,
                    AudioFile.file_type,
                )
                .join(UserAudioFile, UserAudioFile.upload_id == UserRawUploadedFile.id)
                .join(AudioFile, UserAudioFile.audio_file_id == AudioFile.id)
                .join(User, UserAudioFile.user_id == User.id)
                .filter(tsvector.op("@@")(tsquery))
            )
            if user_id:
               query = query.filter(UserAudioFile.user_id == user_id) 

            query = (
                 query         
                .order_by(desc(UserRawUploadedFile.created_at),desc(AudioFile.file_type))
                .limit(limit)
                .offset(offset)
             )

            # Execute the query and return the results
            results = await read_session.execute(query)
            return results.all()
