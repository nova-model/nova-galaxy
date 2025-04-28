"""Utilities."""

from enum import Enum


class WorkState(Enum):
    """The state of a tool in Galaxy."""

    NOT_STARTED = "not_started"
    UPLOADING_DATA = "uploading"
    QUEUED = "queued"
    RUNNING = "running"
    FINISHED = "finished"
    ERROR = "error"
    DELETED = "deleted"
    CANCELED = "canceled"
    STOPPING = "stopping"
    CANCELING = "canceling"
