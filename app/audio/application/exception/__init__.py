from core.exceptions import CustomException


class MissingPolicyException(CustomException):
    code = 500
    error_code = "AUDIO__MISSING_POLICY"
    message = "Missing policy."


class FileNotFound(CustomException):
    code = 404
    error_code = "AUDIO__FILE_NOT_FOUND"
    message = "File not found"
