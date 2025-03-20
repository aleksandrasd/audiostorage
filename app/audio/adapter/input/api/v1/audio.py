import asyncio
from collections import defaultdict
import os
import tempfile
from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, File, Path, Query, Request, Response, UploadFile
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.audio.adapter.input.api.v1.response import UserAudioResponse
from app.audio.application.dto import AudioUploadResponseDTO
from app.audio.domain.command import UploadAudioCommand
from app.audio.domain.entity.audio_file import AudioFileRead
from app.audio.domain.usecase.audio import AudioServiceUseCase
from app.container import Container
from celery_task import celery_app
from celery_task.name import CONVERT_AUDIO
from core.fastapi.dependencies.permission import IsAuthenticated, PermissionDependency
from core.helpers.audio import AudioHelper
from core.helpers.string import convert_seconds_to_hms

router = APIRouter()

@router.post(
    "/upload",
    summary = "Upload audio",
    description="Uploads audio and converts audio to appropriate audio formats",
    response_model=AudioUploadResponseDTO,
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
@inject
async def upload_audio(
    request: Request,
    file: UploadFile = File(...),
    usecase: AudioServiceUseCase = Depends(Provide[Container.audio_service]),
):
    user_id = 1
    upload_command = UploadAudioCommand(
        data=file.file,
        len=os.fstat(file.file.fileno()).st_size,
        name=file.filename,
        user_id=user_id,
    )
    upload_id = await usecase.upload_audio(upload_command)
    task = await asyncio.to_thread(
        celery_app.send_task,
        CONVERT_AUDIO,
        kwargs={"user_id": user_id, "upload_id": upload_id},
    )
    return {"task_id": task.id}


@router.get("/download/{id}",
    summary = "Download audio",
    description="Downloads audio with specified name",
    response_model=FileResponse)
@inject
async def download_file(
    response: Response,
    id: str,
    file_name: str,
    usecase: AudioServiceUseCase = Depends(Provide[Container.audio_service]),
):
    temp_file = tempfile.mktemp()
    await usecase.download_audio_file(id, temp_file)
    download_file_name = await usecase.get_download_file_name(id)
    return FileResponse(
        temp_file, filename=download_file_name, media_type="application/octet-stream"
    )



@router.get("/me/audio",
    summary = "List uploaded audio",
    description="List uploaded audio.",
    response_model=FileResponse)
@inject
async def list_my_audio(
    request: Request,
    usecase: AudioServiceUseCase = Depends(Provide[Container.audio_service]),
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))]
):
    audio_files = await usecase.list_audio_files(user_id= request.user.id)
    return AudioHelper.format_file_list(audio_files)

@router.get("/users/{user_id}/audio",
    summary = "List specified user's audio",
    description="List specified user's audio",
    response_model = list[UserAudioResponse])
@inject
async def list_user_audio(
    request: Request,
    usecase: AudioServiceUseCase = Depends(Provide[Container.audio_service]),
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))]
):
    audio_files = await usecase.list_audio_files(user_id= request.user.id)
    return AudioHelper.format_file_list(audio_files)


@router.get("/search",
    summary = "Search audio",
    description="Conduct full text search for an audio.",
    response_model = list[UserAudioResponse])
@inject
async def search_audio(
    request: Request,
    q: str = Query(..., description="Search query"),
    usecase: AudioServiceUseCase = Depends(Provide[Container.audio_service]),
):
    audio_files = await usecase.files_full_text_search(q)
    return AudioHelper.format_file_list(audio_files)