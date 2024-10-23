import importlib.metadata

from .nova import NOVA

__all__ = ["NOVA"]

__version__ = importlib.metadata.version(__package__)
