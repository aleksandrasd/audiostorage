import asyncio
from collections import defaultdict
import os
import tempfile
from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Cookie, Depends, File, Path, Query, Request, Response, UploadFile
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


from app.audio.adapter.input.api.v1.exception import AudioFileNotFound
from app.audio.adapter.input.api.v1.response import AudioFilesPaginationResponse
from app.audio.application.dto import AudioUploadResponseDTO
from app.audio.domain.command import UploadAudioCommand
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
    description="Uploads any media file and converts to appropriate audio formats.",
    response_model=AudioUploadResponseDTO,
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
    status_code=status.HTTP_202_ACCEPTED
)
@inject
async def upload_audio(
    request: Request,
    id: str = Cookie(..., title = "User ID", description="User ID"),
    file: UploadFile = File(..., title = "Media file", description="Takes any media file and uploads as an audio"),
    usecase: AudioServiceUseCase = Depends(Provide[Container.audio_service]),
):
    upload_command = UploadAudioCommand(
        data=file.file,
        len=os.fstat(file.file.fileno()).st_size,
        name=file.filename,
        user_id=id,
    )
    upload_id = await usecase.upload_audio(upload_command)
    task = await asyncio.to_thread(
        celery_app.send_task,
        CONVERT_AUDIO,
        kwargs={"user_id": id, "upload_id": upload_id},
    )
    return {"task_id": task.id}


@router.get("/download/{id}/{file_name}",
    summary = "Download audio",
    description="Downloads audio")
@inject
async def download_file(
    response: Response,
    id: str = Path(..., title = "File ID", description="The ID of the audio to be downloaded"),
    file_name: str = Path(..., title = "File name", description="The file name of the audio to be downloaded"),
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
    response_model=AudioFilesPaginationResponse)
@inject
async def list_my_audio(
    request: Request,
    id: str = Cookie(..., title = "User ID", description="User ID"),
    usecase: AudioServiceUseCase = Depends(Provide[Container.audio_service]),
    page: int = Query(10, title="Page number", description="Audio search result page number to return"),
    per_page: int = Query(0, title="Maximum audio files per page", description="Maximum audio files to return per one page."), 
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))]
):
    counted_audio_files = await usecase.list_audio_files(user_id = id, page = page, per_page = per_page) 
    return AudioHelper.create_audio_files_pagination_response(counted_audio_files) 

@router.get("/user/{user_id}/audio",
    summary = "List specified user's audio",
    description="List specified user's audio",
    response_model = AudioFilesPaginationResponse)
@inject
async def list_user_audio(
    request: Request,
    user_id: int = Path(..., title = "Used ID", description = "User ID of an user whose audios"),
    page: int = Query(10, title="Page number", description="Audio search result page number to return"),
    per_page: int = Query(0, title="Maximum audio files per page", description="Maximum audio files to return per one page."), 
    usecase: AudioServiceUseCase = Depends(Provide[Container.audio_service]),
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))]
):
    counted_audio_files = await usecase.list_audio_files(user_id = user_id, page = page, per_page = per_page) 
    return AudioHelper.create_audio_files_pagination_response(counted_audio_files) 




@router.get("/search",
    summary = "Search audio",
    description="Conduct full text search for an audio.",
    response_model = AudioFilesPaginationResponse)
@inject 
async def search_audio(
    request: Request,
    q: str = Query(..., title="Query string", description="Query string for search audio by name"),
    page: int = Query(10, title="Page number", description="Audio search result page number to return"),
    per_page: int = Query(0, title="Maximum audio fil es per page", description="Maximum audio files to return per one page."), 
    usecase: AudioServiceUseCase = Depends(Provide[Container.audio_service]),
):
    counted_audio_files = await usecase.files_full_text_search(q, None, page = page, per_page = per_page)
    return AudioHelper.create_audio_files_pagination_response(counted_audio_files) 