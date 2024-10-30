"""
    Tool
"""

from typing import Dict, List

from bioblend import galaxy

from .dataset import Dataset
from .data_store import Datastore
from .parameters import Parameters



class AbstractWork:

    def __init__(self, id: str):
        self.id = id

    def get_outputs(self) -> List[Dataset]:
        return []

    def get_inputs(self) -> List[Parameters]:
        return []

    def run(self, data_store: Datastore, params: Parameters) -> Dict[str, Dataset]:
        return {}


class Tool(AbstractWork):

    def __init__(self, id: str):
        super().__init__(id)

    def run(self, data_store: Datastore, params: Parameters) -> Dict[str, Dataset]:
        galaxy_instance = data_store.nova.galaxy_instance
        history_id = galaxy_instance.histories.get_histories(name=data_store.name)[0]["id"]
        dataset_client = galaxy.datasets.DatasetClient(galaxy_instance)

        dataset_ids = []
        tool_inputs = galaxy.tools.inputs.inputs()
        for param, dataset in params.inputs.items():
            dataset_id = galaxy_instance.tools.upload_file(dataset.path, data_store.name)
            dataset_ids.append(dataset_id)
            tool_inputs.set_dataset_param(param, dataset_id)
        for dataset in dataset_ids:
            dataset_client.wait_for_dataset(dataset)

        results = galaxy_instance.run_tool(history_id, self.id, tool_inputs)

        # Could handle this better
        galaxy_instance.jobs.wait_for_job(job_id=results['creating_job'])
        outputs = {}
        result_collections = results['output_collections']
        result_datasets = results['outputs']
        if result_datasets:
            for ds in result_datasets:
                d = Dataset("")
                d.id = ds['id']
                outputs[ds["name"]] = d
        if result_collections:
            for dsc in result_collections:
                d = Dataset("")
                d.id = dsc['id']
                outputs[ds["name"]] = d

        return outputs
