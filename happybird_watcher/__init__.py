"""HappyBird Watcher - A SyftBox app for monitoring happybird.txt files"""

from .widgets import HappyBirdWatcher
from .endpoints import (
    get_happybird_files,
    get_happybird_content,
    get_happybird_stats
)

__version__ = "0.1.0"

# Define what gets imported with "from happybird_watcher import *"
__all__ = [
    "HappyBirdWatcher",
    "get_happybird_files", 
    "get_happybird_content",
    "get_happybird_stats"
]
