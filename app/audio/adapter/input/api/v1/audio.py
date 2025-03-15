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

# from app.audio.adapter.input.celery import convert_audio
from app.audio.adapter.input.api.v1.response import UserAudioResponse
from app.audio.application.dto import AudioUploadResponseDTO
from app.audio.domain.command import UploadAudioCommand
from app.audio.domain.entity.audio_file import AudioFileRead
from app.audio.domain.usecase.audio import AudioServiceUseCase
from app.container import Container
from celery_task import celery_app
from celery_task.name import CONVERT_AUDIO
from core.fastapi.dependencies.permission import IsAuthenticated, PermissionDependency
from core.helpers.string import convert_seconds_to_hms

router = APIRouter()

@router.post(
    "/upload",
    response_model=AudioUploadResponseDTO,
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
@inject
async def upload_audio(
    request: Request,
    file: UploadFile = File(...),
    usecase: AudioServiceUseCase = Depends(Provide[Container.audio_service]),
):
    user_id = request.user.id
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


@router.get("/download/{file_name}/{original_file_name}")
@inject
async def download_file(
    response: Response,
    file_name: str,
    original_file_name: str,
    usecase: AudioServiceUseCase = Depends(Provide[Container.audio_service]),
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
) -> FileResponse:
    temp_file = temp_file_name = tempfile.mktemp()
    await usecase.download_audio_file(file_name, temp_file)
    return FileResponse(
        temp_file, filename=original_file_name, media_type="application/octet-stream"
    )


@router.get("/list_user_audio",
            dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
            response_model=list[UserAudioResponse])
@inject
async def list_user_audio(
    request: Request,
    usecase: AudioServiceUseCase = Depends(Provide[Container.audio_service]),
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))]
):
    user_id = request.user.id
    audio_files = await usecase.list_audio_files(user_id=user_id)
    grouped_files = defaultdict(list)
    for file in audio_files:
        audio = file.model_dump()
        base_name =os.path.splitext(audio['original_file_name'])[0]  
        audio['base_name'] = base_name
        audio['actual_file_name'] =  f"{base_name}.{audio['file_type']}"
        grouped_files[str(file.created_at)].append(audio)
UserAudioResponse
    return grouped_files





@router.get("/search",
            dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
            response_model = list[AudioFileRead])
@inject
async def search_audio(
    request: Request,
    q: str = Query(..., description="Search query"),
    usecase: AudioServiceUseCase = Depends(Provide[Container.audio_service]),
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))]
):
    audio_files = await usecase.files_full_text_search(q)

    grouped_files = defaultdict(list)
    for file in audio_files:
        audio = file.model_dump()
        base_name =os.path.splitext(audio['original_file_name'])[0]  
        audio['base_name'] = base_name
        audio['new_ext_name'] =  f"{base_name}.{audio['file_type']}"
        grouped_files[str(file.created_at)].append(audio)

    return grouped_files
