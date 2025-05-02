from core.exceptions import CustomException


class MissingPolicyException(CustomException):
    code = 500
    error_code = "AUDIO__MISSING_POLICY"
    message = "Missing policy."

class AudioFileNotFound(CustomException):
    code = 404
    error_code = "AUDIO__FILE_NOT_FOUND"
    message = "Audio file not found"