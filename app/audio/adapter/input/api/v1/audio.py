from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, File, Request, UploadFile

from app.audio.adapter.input.celery.audio import convert_audio
from app.audio.application.dto import AudioUploadResponseDTO
from app.audio.domain.command import ConvertAudioCommand, UploadAudioCommand
from app.audio.domain.usecase.audio import AudioServiceUseCase
from app.container import Container

router = APIRouter()


@router.post(
    "/upload",
    response_model=AudioUploadResponseDTO,
    # dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
@inject
def upload_audio(
    request: Request,
    file: UploadFile = File(...),
    usecase: AudioServiceUseCase = Depends(Provide[Container.audio_service]),
):
    # Validate file size
    # try:
    #     max_size = await usecase.get_max_audio_file_size()
    # except Exception as e:
    #     raise HTTPException(
    #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #         detail="Failed to retrieve max size file policy"
    # )
    # content_length = request.headers.get("content-length")
    # if not content_length or not content_length.isdigit():
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Content-Length")

    # if file_size > max_size:
    #     raise HTTPException(
    #         status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
    #         detail=f"File exceeds maximum size of {max_size} bytes"
    # )
    # Generate unique filename and upload to Minio
    user_id = 1  # request.user.id
    upload_command = UploadAudioCommand(
        data=file,
        len=request.headers.get("content-length"),
        name=file.filename,
        user_id=user_id,
    )
    usecase.upload_audio(upload_command)
    convert_command = ConvertAudioCommand(
        user_id=user_id, file_name=file.filename, audio_types=["wav", "mp3"]
    )
    task = convert_audio.apply_async((convert_command,))  # Async task execution
    return {"task_id": task.id}
