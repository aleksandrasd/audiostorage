from typing import List

from sqlalchemy import select

from app.audio.domain.entity.audio_file import (
    AudioFile,
    AudioFileMeta,
    Policy,
    UserAudioFile,
    UserRawUploadedFile,
)
from app.audio.domain.repository.audio import AudioRepo
from core.db.session import session, session_factory


class AudioSQLAlchemyRepo(AudioRepo):
    def save_upload_music_file_record(
        self, user_raw_uploaded_file: UserRawUploadedFile
    ) -> None:
        session.add(user_raw_uploaded_file)

    def save_audio_file_meta(self, audio_file_meta: AudioFileMeta) -> None:
        session.add(audio_file_meta)

    def save_audio_file(self, audio_file: AudioFile) -> None:
        session.add(audio_file)

    def save_user_audio_file(self, user_audio_file: UserAudioFile) -> None:
        session.add(user_audio_file)

    def persist(self) -> None:
        session.flush()

    def get_audio_upload_file_max_size(self) -> int | None:
        with session_factory() as read_session:
            return read_session.query(Policy.upload_max_size_in_bytes).first()

    def get_audio_formats_for_download(self) -> List[str] | None:
        with session_factory() as read_session:
            return read_session.query(Policy.audio_formats_download).first()

    def get_raw_audio_id(name: str) -> int:
        query = select(UserRawUploadedFile.id).where(
            UserRawUploadedFile.file_name == name
        )
        return session.execute(query).scalar()
