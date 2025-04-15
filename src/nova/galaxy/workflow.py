from .job import Job
from .outputs import Outputs
from .parameters import Parameters
from .tool import AbstractWork
from .util import WorkState

from typing import Optional

class Workflow(AbstractWork):
    
    def __init__(self, id: str):
        super().__init__(id)
        self._job: Optional[Job] = None
        
    def run(self, data_store: "Datastore", params: Optional[Parameters] = None, wait: bool = True) -> Optional[Outputs]:
        """Run this tool.

        By default, will be run in a blocking manner, unless `wait` is set to False. Will return the
        results as an instance of the `Outputs` class from nova.galaxy.outputs if run in a blocking way. Otherwise, will
        return None, and the user will be responsible for getting results by calling `get_results`.

        Parameters
        ----------
        data_store: Datastore
            The data store to run this tool in.
        params: Parameters
            The input parameters for this tool.
        wait: bool
            Whether to run this tool in a blocking manner (True) or not (False). Default is True.

        Returns
        -------
        Optional[Outputs]
            If run in a blocking manner, returns the Outputs once the tool is finished running. Otherwise, returns None.

        """
        self._job = Job(self.id, data_store)
        params.workflow_parameter_set = True
        return self._job.run(params, wait)

    def get_status(self) -> WorkState:
        """Returns the current status of the tool.

        Returns
        -------
        WorkState
           Returns the status of the tool which will be one of the following values: not_started, uploading, queued,
           running, finished, error
        """
        if self._job:
            return self._job.get_state().state
        else:
            return WorkState.NOT_STARTED
        
    def stop(self) -> None:
        """Stop the tool, but keep any existing results."""
        if self._job:
            self._job.cancel(check_results=True)

    def cancel(self) -> None:
        """Cancels the tool execution and gets rid of any results collected."""
        if self._job:
            self._job.cancel(check_results=False)

    def get_stdout(self) -> Optional[str]:
        """Get the current STDOUT for a tool.

        Will be overridden everytime this tool is run.

        Returns
        -------
        Optional[str]
           Returns the current STDOUT of the tool if it is running or finished.
        """
        if self._job:
            return self._job.get_console_output()["stdout"]
        return None

    def get_stderr(self) -> Optional[str]:
        """Get the current STDERR for a tool.

        Will be overridden everytime this tool is run.

        Returns
        -------
        Optional[str]
           Returns the current STDERR of the tool if it is running or finished.
        """
        if self._job:
            return self._job.get_console_output()["stderr"]
        return None
