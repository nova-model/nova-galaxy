import importlib.metadata

from .nova import Nova

__all__ = ["Nova"]


__version__ = importlib.metadata.version("nova-galaxy")
