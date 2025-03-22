from core.exceptions import CustomException


class MissingPolicyException(CustomException):
    code = 500
    error_code = "AUDIO__MISSING_POLICY"
    message = "Missing policy."

