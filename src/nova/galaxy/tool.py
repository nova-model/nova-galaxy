"""
    Tool
"""

from typing import Any, Dict, List

from bioblend import galaxy

from .dataset import AbstractData, Dataset, DatasetCollection, upload_datasets
from .data_store import Datastore
from .parameters import Parameters



class AbstractWork:

    def __init__(self, id: str):
        self.id = id

    def get_outputs(self) -> List[AbstractData]:
        return []

    def get_inputs(self) -> List[Parameters]:
        return []

    def run(self, data_store: Datastore, params: Parameters) -> Dict[str, AbstractData]:
        return {}


class Tool(AbstractWork):

    def __init__(self, id: str):
        super().__init__(id)

    def run(self, data_store: Datastore, params: Parameters) -> Dict[Any, AbstractData]:
        outputs: Dict[Any, AbstractData] = {}
        galaxy_instance = data_store.nova.galaxy_instance
        history_id = galaxy_instance.histories.get_histories(name=data_store.name)[0]["id"]

        datasets_to_upload = {}

        # Set Tool Inputs
        tool_inputs = galaxy.tools.inputs.inputs()
        for param, val in params.inputs.items(): 
            if isinstance(val, AbstractData):
                datasets_to_upload[param] = val
            else: 
                tool_inputs.set_param(param, val)

        ids = upload_datasets(store=data_store, datasets=datasets_to_upload)
        for param, val  in ids.items():
            tool_inputs.set_param(param, val)

        # Run tool and wait for job to finish
        results = galaxy_instance.run_tool(history_id, self.id, tool_inputs)

        galaxy_instance.jobs.wait_for_job(job_id=results['creating_job'])
        

        # Collect output datasets and dataset collections
        result_collections = results['output_collections']
        result_datasets = results['outputs']
        if result_datasets:
            for dataset in result_datasets:
                d = Dataset("")
                d.id = dataset['id']
                outputs[dataset["name"]] = d
        if result_collections:
            for collection in result_collections:
                dc = DatasetCollection("")
                dc.id = collection['id']
                outputs[collection["name"]] = d

        return outputs
