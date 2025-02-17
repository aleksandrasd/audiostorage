from enum import Enum


class TaskState(str, Enum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    RETRY = "RETRY"
    STARTED = "STARTED"
    REVOKED = "REVOKED"
