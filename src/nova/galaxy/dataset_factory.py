from typing import Optional

from bioblend import galaxy

from .parameters import Parameters

class DatasetFactory():
    
    @staticmethod
    def create_dataset(store, config):
        
        # Avoid circular imports for this singleton class by importing packages after declaration
        from .dataset import Dataset
        
        d = Dataset(config["output_name"])
        d.id = config["id"]
        d.store = store
        return d
    
    @staticmethod
    def create_dataset_collection(store, config):
        
        # Avoid circular imports for this singleton class by importing packages after declaration
        from .dataset import DatasetCollection
        
        dc = DatasetCollection([], config["output_name"])
        dc.id = config["id"]
        dc.store = store
        return dc

    @staticmethod
    def upload_data(store, params: Optional[Parameters]):
    
        # Avoid circular imports for this singleton class by importing packages after declaration
        from .dataset import Dataset, DatasetCollection, upload_datasets

        datasets_to_upload = {}

        # Set Tool Inputs
        tool_inputs = galaxy.tools.inputs.inputs()
        if params:
            for param, val in params.inputs.items():
                if isinstance(val, Dataset):
                    datasets_to_upload[param] = val
                elif isinstance(val, DatasetCollection):
                    val.upload(store)
                    tool_inputs.set_dataset_param(param, val.id)
                else:
                    tool_inputs.set_param(param, val)
            ids = upload_datasets(store=store, datasets=datasets_to_upload)
            for param, val in ids.items():
                tool_inputs.set_dataset_param(param, val)

        return tool_inputs
