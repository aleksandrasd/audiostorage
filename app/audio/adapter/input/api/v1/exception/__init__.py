from core.exceptions.base import CustomException


class AudioFileNotFound(CustomException):
    code = 404
    error_code = "AUDIO__FILE_NOT_FOUND"
    message = "Audio file not found"