"""Contains classes to run tools in Galaxy via Nova."""

import time
from typing import List, Union

from bioblend import galaxy

from .data_store import Datastore
from .dataset import AbstractData, Dataset, DatasetCollection, upload_datasets
from .outputs import Outputs
from .parameters import Parameters


class AbstractWork:
    """Abstraction for a runnable object in Galaxy such as a tool or workflow."""

    def __init__(self, id: str):
        self.id = id

    def get_outputs(self) -> List[AbstractData]:
        return []

    def get_inputs(self) -> List[Parameters]:
        return []

    def run(self, data_store: Datastore, params: Parameters) -> Union[Outputs, None]:
        return None


class Tool(AbstractWork):
    """Represents a tool from Galaxy that can be run."""

    def __init__(self, id: str):
        super().__init__(id)

    def run(self, data_store: Datastore, params: Parameters) -> Outputs:
        """Runs this tool in a blocking manner and returns a map of the output datasets and collections."""
        outputs = Outputs()
        galaxy_instance = data_store.nova_connection.galaxy_instance
        datasets_to_upload = {}

        # Set Tool Inputs
        tool_inputs = galaxy.tools.inputs.inputs()
        for param, val in params.inputs.items():
            if isinstance(val, AbstractData):
                datasets_to_upload[param] = val
            else:
                tool_inputs.set_param(param, val)

        ids = upload_datasets(store=data_store, datasets=datasets_to_upload)
        for param, val in ids.items():
            tool_inputs.set_dataset_param(param, val)

        # Run tool and wait for job to finish
        results = galaxy_instance.tools.run_tool(
            history_id=data_store.history_id, tool_id=self.id, tool_inputs=tool_inputs
        )

        for job in results["jobs"]:
            galaxy_instance.jobs.wait_for_job(job_id=job["id"])

        # Collect output datasets and dataset collections
        result_datasets = results["outputs"]
        result_collections = results["output_collections"]
        if result_datasets:
            for dataset in result_datasets:
                d = Dataset(dataset["output_name"])
                d.id = dataset["id"]
                d.store = data_store
                outputs.add_output(d)
        if result_collections:
            for collection in result_collections:
                dc = DatasetCollection(collection["output_name"])
                dc.id = collection["id"]
                dc.store = data_store
                outputs.add_output(dc)

        return outputs

    def run_interactive(self, data_store: Datastore, params: Parameters, max_tries: int = 100) -> str:
        galaxy_instance = data_store.nova_connection.galaxy_instance
        datasets_to_upload = {}
        # Set Tool Inputs
        tool_inputs = galaxy.tools.inputs.inputs()
        for param, val in params.inputs.items():
            if isinstance(val, AbstractData):
                datasets_to_upload[param] = val
            else:
                tool_inputs.set_param(param, val)

        ids = upload_datasets(store=data_store, datasets=datasets_to_upload)
        for param, val in ids.items():
            tool_inputs.set_dataset_param(param, val)

        # Run tool and wait for job to finish
        results = galaxy_instance.tools.run_tool(
            history_id=data_store.history_id, tool_id=self.id, tool_inputs=tool_inputs
        )
        job_id = results["jobs"][0]["id"]

        timer = max_tries
        while timer > 0:
            entry_points = galaxy_instance.make_get_request(
                f"{data_store.nova_connection.galaxy_url}/api/entry_points?job_id={job_id}"
            )
            for ep in entry_points.json():
                if ep["job_id"] == job_id and ep.get("target", None):
                    return f"{data_store.nova_connection.galaxy_url}{ep['target']}"
            timer -= 1
            time.sleep(1)
        status = galaxy_instance.jobs.cancel_job(job_id)
        # if status is false, the job has been in a terminal state already, indicating an error somewhere in execution
        if status:
            raise Exception("Unable to fetch the URL for interactive tool.")
        else:
            raise Exception("Interactive tool was stopped unexpectedly.")


def stop_all_tools_in_store(data_store: Datastore) -> None:
    galaxy_instance = data_store.nova_connection.galaxy_instance
    jobs = galaxy_instance.jobs.get_jobs(history_id=data_store.history_id)
    for job in jobs:
        galaxy_instance.jobs.cancel_job(job["id"])
