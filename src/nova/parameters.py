"""
Parameters
"""


from .dataset import Dataset
from typing import Dict, Union


class Parameters:
    """this class is justa specialized map wrapper basically"""

    def __init__(self) -> None:
        self.inputs: Dict[str, Union[str, int, bool, AbstractData]] = {}


    def add_input(self, name: str, dataset: Dataset) -> None:
        self.inputs[name] = dataset


    def change_input_value(self, name: str, new_dataset: Dataset) -> None:
        if self.inputs[name]:
            self.inputs[name] = new_dataset


    def remove_input(self, name: str) -> None:
        self.inputs.pop(name)

