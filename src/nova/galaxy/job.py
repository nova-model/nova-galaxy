"""
Job
"""

from .data_store import Datastore
from .parameters import Parameters
from .tool import AbstractWork


class Job:
    def __init__(self, work: AbstractWork):
        pass

    def submit_job(self, datastore: Datastore, params: Parameters) -> None:
        pass

    def cancel_job(self) -> None:
        pass

    def wait_for_job(self) -> None:
        pass

    def get_state(self) -> None:
        pass

    def get_outputs(self) -> None:
        pass

    def get_stdout(self) -> str:
        pass

    def get_stderr(self) -> str:
        pass

    def get_results(self) -> None:
        pass
