from fastapi import Depends, FastAPI, Request
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.audio.adapter.input.api import router as audio_router
from app.container import Container
from app.user.adapter.input.api import router as user_router
from core.config import config
from core.exceptions import CustomException
from core.fastapi.dependencies import Logging
from core.fastapi.middlewares import (
    AuthBackend,
    AuthenticationMiddleware,
    SQLAlchemyMiddleware,
)
from core.fastapi.middlewares.authentication import CustomMiddleware
from core.helpers.cache import Cache, CustomKeyMaker, RedisBackend
from core.web import frontend_router


def init_routers(app_: FastAPI) -> None:
    container = Container()
    user_router.container = container
    audio_router.container = container
    app_.include_router(user_router)
    app_.include_router(audio_router)
    app_.include_router(frontend_router)


def init_listeners(app_: FastAPI) -> None:
    # Exception handler
    @app_.exception_handler(CustomException)
    async def custom_exception_handler(request: Request, exc: CustomException):
        return JSONResponse(
            status_code=exc.code,
            content={"error_code": exc.error_code, "message": exc.message},
        )


def on_auth_error(request: Request, exc: Exception):
    status_code, error_code, message = 401, None, str(exc)
    if isinstance(exc, CustomException):
        status_code = int(exc.code)
        error_code = exc.error_code
        message = exc.message

    return JSONResponse(
        status_code=status_code,
        content={"error_code": error_code, "message": message},
    )


def make_middleware() -> list[Middleware]:
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        ),
        Middleware(
          CustomMiddleware  
        ),
        Middleware(
            AuthenticationMiddleware,
            backend=AuthBackend(),
            on_error=on_auth_error,
        ),
        Middleware(SQLAlchemyMiddleware),  # ,
        # Middleware(ResponseLogMiddleware),
    ]
    return middleware


def init_cache() -> None:
    Cache.init(backend=RedisBackend(), key_maker=CustomKeyMaker())


def create_app() -> FastAPI:
    app_ = FastAPI(
        title="Audio Storage",
        summary="Audio Storage is a FastAPI application that lets users upload, store, and search for audio files. It accepts both audio and video uploads, automatically converting them into standard audio formats like WAV and MP3 before saving. Users can easily discover and access audio shared by others through built-in search functionality.",
        description="""
Audio Storage is a application that enables users to upload, store, and search for audio files shared by others. The platform supports uploading various media formats, including audio and video files, and automatically converts them into commonly used audio formats such as WAV and MP3 for standardized storage.
Features:

* Upload Media: Supports both audio and video uploads, ensuring compatibility with various formats.
* Automatic Conversion: Converts uploaded media to WAV and MP3 before storage.
* Search Functionality: Allows users to find audio files stored by others based on file names.
""",
        version="1.0.0",
        docs_url=None if config.ENV == "production" else "/docs",
        redoc_url=None if config.ENV == "production" else "/redoc",
        dependencies=[Depends(Logging)],
        middleware=make_middleware(),
    )
    app_.mount("/static", StaticFiles(directory="frontend/static"), name="static")
    init_routers(app_=app_)
    init_listeners(app_=app_)
    init_cache()
    return app_


app = create_app()
