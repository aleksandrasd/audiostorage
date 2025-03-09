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
from app.audio.application.dto import AudioUploadResponseDTO
from app.audio.domain.command import UploadAudioCommand
from app.audio.domain.entity.audio_file import AudioFileRead
from app.audio.domain.usecase.audio import AudioServiceUseCase
from app.container import Container
from celery_task import celery_app
from celery_task.name import CONVERT_AUDIO
from core.helpers.string import convert_seconds_to_hms

router = APIRouter()


# Mount static files (if you have CSS/JS)
router.mount("/static", StaticFiles(directory="static"), name="static")
# Set up Jinja2 templates
templates = Jinja2Templates(directory="static/templates")


@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.post(
    "/upload",
    response_model=AudioUploadResponseDTO,
    # dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
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
    # task = await asyncio.to_thread(
    #     convert_audio.delay,
    #     user_id=user_id,
    #     file_name=file.filename,
    #     audio_types=["wav", "mp3"]
    # )
    return {"task_id": task.id}


@router.get("/download/{file_name}/{original_file_name}")
@inject
async def download_file(
    response: Response,
    file_name: str,
    original_file_name: str,
    usecase: AudioServiceUseCase = Depends(Provide[Container.audio_service]),
) -> FileResponse:
    temp_file = temp_file_name = tempfile.mktemp()
    await usecase.download_audio_file(file_name, temp_file)
    return FileResponse(
        temp_file, filename=original_file_name, media_type="application/octet-stream"
    )


@router.get("/list_audio")
@inject
async def list_audio(
    usecase: AudioServiceUseCase = Depends(Provide[Container.audio_service])
) -> List[AudioFileRead]:
    return await usecase.list_audio_files()


@router.get("/list_user_audio")
@inject
async def list_user_audio(
    request: Request,
    usecase: AudioServiceUseCase = Depends(Provide[Container.audio_service])
) -> List[AudioFileRead]:
    audio_files = await usecase.list_audio_files(user_id=1)
    grouped_files = defaultdict(list)
    for file in audio_files:
        audio = file.model_dump()
        base_name =os.path.splitext(audio['original_file_name'])[0]  
        audio['base_name'] = base_name
        audio['new_ext_name'] =  f"{base_name}.{audio['file_type']}"
        grouped_files[str(file.created_at)].append(audio)

    return templates.TemplateResponse("list.html", {"request": request, "grouped_files": grouped_files})


@router.get("/search")
@inject
async def search_audio(
    request: Request,
    q: str = Query(..., description="Search query"),
    usecase: AudioServiceUseCase = Depends(Provide[Container.audio_service]),
) -> List[AudioFileRead]:
    audio_files = await usecase.files_full_text_search(q)

    grouped_files = defaultdict(list)
    for file in audio_files:
        audio = file.model_dump()
        base_name =os.path.splitext(audio['original_file_name'])[0]  
        audio['base_name'] = base_name
        audio['new_ext_name'] =  f"{base_name}.{audio['file_type']}"
        grouped_files[str(file.created_at)].append(audio)

    return templates.TemplateResponse("list.html", {"request": request, "grouped_files": grouped_files})
