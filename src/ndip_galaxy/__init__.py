import importlib.metadata

from .ndip import NDIP

__all__ = ["NDIP"]

__version__ = importlib.metadata.version(__package__)
