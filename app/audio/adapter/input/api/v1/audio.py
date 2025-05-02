import asyncio
from collections import defaultdict
import os
import tempfile
from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Cookie, Depends, File, Path, Query, Request, Response, UploadFile
from fastapi.responses import FileResponse

from app.audio.adapter.input.api.v1.response import AudioFilesPaginationResponse
from app.audio.application.dto import AudioUploadResponseDTO
from app.audio.application.exception import AudioFileNotFound
from app.audio.domain.command import RemoveAudioCommand, UploadAudioCommand
from app.audio.domain.usecase.audio import AudioServiceUseCase
from app.container import Container
from celery_task import celery_app
from celery_task.name import CONVERT_AUDIO
from core.fastapi.dependencies.permission import IsAuthenticated, PermissionDependency
from core.helpers.audio import AudioHelper
from core.helpers.string import convert_seconds_to_hms
from fastapi import status

router = APIRouter()

@router.post(
    "/upload",
    summary = "Upload audio",
    description="Stores audio files. Supports uploading audio and video file, converts to wav and mp3 before storing.",
    response_model=AudioUploadResponseDTO,
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
    status_code=status.HTTP_202_ACCEPTED
)
@inject
async def upload_audio(
    request: Request,
    file: UploadFile = File(..., title = "Media file", description="Takes any media file and uploads as an audio"),
    usecase: AudioServiceUseCase = Depends(Provide[Container.audio_service]),
):
    upload_command = UploadAudioCommand(
        data=file.file,
        len=os.fstat(file.file.fileno()).st_size,
        name=file.filename,
        user_id=request.user.id,
    )
    upload_id = await usecase.upload_audio(upload_command)
    task = await asyncio.to_thread(
        celery_app.send_task,
        CONVERT_AUDIO,
        kwargs={"user_id": request.user.id  , "upload_id": upload_id},
    )
    return {"task_id": task.id}


@router.get("/download/{id}/{file_name}",
    summary = "Download audio",
    description="This API allows clients to download an audio file by specifying its unique id and associated file name.",
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))])
@inject
async def download_file(
    response: Response,
    id: str = Path(..., title = "File ID", description="Unique identifier of the audio file."),
    file_name: str = Path(..., title = "File name", description="The exact name of the audio file, including extension (e.g., track01.mp3)."),
    usecase: AudioServiceUseCase = Depends(Provide[Container.audio_service]),
) -> FileResponse:
    download_file_name = await usecase.get_download_file_name(id)
    if not download_file_name or download_file_name != file_name:
        raise AudioFileNotFound
    temp_file = tempfile.mktemp()
    await usecase.download_audio_file(id, temp_file)
    return FileResponse(
        temp_file, filename=download_file_name, media_type="application/octet-stream"
    )



@router.get("/me/audio",
    summary = "List user's uploaded audio",
    description="List user's uploaded audio.",
    response_model=AudioFilesPaginationResponse,
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))])
@inject
async def list_my_audio(
    request: Request,
    usecase: AudioServiceUseCase = Depends(Provide[Container.audio_service]),
    page: int = Query(1, title="Page number", description="Audio search result page number to return"),
    per_page: int = Query(10, title="Maximum audio files per page", description="Maximum audio files to return per one page.")
):
    counted_audio_files = await usecase.list_audio_files(user_id = request.user.id, page = page, per_page = per_page) 
    return AudioHelper.create_audio_files_pagination_response(counted_audio_files) 


@router.get("/user/{nickname}/audio",
    summary = "List specified user's audio",
    description="List specified user's audio",
    response_model = AudioFilesPaginationResponse,
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))])
@inject
async def list_user_audio(
    request: Request,
    nickname: str = Path(..., title = "Nickname", description = "Nickname of an user whose audio files collection to return."),
    page: int = Query(1, title="Page number", description="Audio search result page number to return"),
    per_page: int = Query(10, title="Maximum audio files per page", description="Maximum audio files to return per one page."), 
    usecase: AudioServiceUseCase = Depends(Provide[Container.audio_service])
):
    counted_audio_files = await usecase.list_audio_files_by_nickname(nickname = nickname, page = page, per_page = per_page) 
    return AudioHelper.create_audio_files_pagination_response(counted_audio_files) 


@router.get("/user/{nickname}/audio",
    summary = "List specified user's audio",
    description="List specified user's audio",
    response_model = AudioFilesPaginationResponse,
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))])
@inject
async def list_user_audio(
    request: Request,
    nickname: str = Path(..., title = "Nickname", description = "Nickname of an user whose audio files collection to return."),
    page: int = Query(1, title="Page number", description="Audio search result page number to return"),
    per_page: int = Query(10, title="Maximum audio files per page", description="Maximum audio files to return per one page."), 
    usecase: AudioServiceUseCase = Depends(Provide[Container.audio_service])
):
    counted_audio_files = await usecase.list_audio_files_by_nickname(nickname = nickname, page = page, per_page = per_page) 
    return AudioHelper.create_audio_files_pagination_response(counted_audio_files) 

@router.get("/remove/{id}",
    summary = "Remove audio file",
    description="Remove uploaded audio file and converted audio files from system.",
    response_model = AudioFilesPaginationResponse,
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))])
@inject 
async def remove_audio(
    request: Request,
    id: str = Path(..., title = "Audio file id", description = "Id of uploaded audio file to be removed"),
    usecase: AudioServiceUseCase = Depends(Provide[Container.audio_service]),
):
    counted_audio_files = await usecase.remove_audio(user_id = request.user.id, uploaded_audio_file_id =id)