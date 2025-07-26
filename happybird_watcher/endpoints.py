"""API endpoints for HappyBird Watcher - File system monitoring for happybird.txt files"""

import os
import glob
from datetime import datetime
from pathlib import Path
from syft_widget import register_endpoint


def get_syftbox_path():
    """Get the SyftBox root path for the current user"""
    home = os.path.expanduser("~")
    return os.path.join(home, "SyftBox")


@register_endpoint("/api/happybird/files")
def get_happybird_files():
    """Find all happybird.txt files in the SyftBox filesystem

    This endpoint is called in three different contexts:
    1. Checkpoint mode: Returns mock data (no server)
    2. Thread mode: Runs in a local server thread
    3. SyftBox mode: Runs in the SyftBox app server
    """

    # Default mock data for when SyftBox doesn't exist
    mock_data = {
        "files": [
            {
                "path": "~/SyftBox/alice/happybird.txt",
                "modified": "2024-01-15 10:30:00",
                "size": 127,
                "owner": "alice"
            },
            {
                "path": "~/SyftBox/bob/happybird.txt", 
                "modified": "2024-01-15 11:45:00",
                "size": 89,
                "owner": "bob"
            }
        ],
        "total_count": 2,
        "last_scan": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    # If SyftBox doesn't exist, return mock data
    if not os.path.exists(get_syftbox_path()):
        return mock_data

    # In production mode, actually scan the filesystem
    syftbox_path = get_syftbox_path()
    found_files = []

    try:
        # Use glob to find all happybird.txt files recursively
        pattern = os.path.join(syftbox_path, "**/happybird.txt")
        files = glob.glob(pattern, recursive=True)

        for file_path in files:
            try:
                stat = os.stat(file_path)
                # Get the owner from the directory structure
                relative_path = os.path.relpath(file_path, syftbox_path)
                owner = relative_path.split(os.sep)[0] if os.sep in relative_path else "unknown"

                found_files.append({
                    "path": file_path,
                    "modified": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                    "size": stat.st_size,
                    "owner": owner
                })
            except Exception as e:
                # Skip files we can't read
                continue

        # Sort by modification time, newest first
        found_files.sort(key=lambda x: x["modified"], reverse=True)

    except Exception as e:
        # If we can't scan, return empty list
        pass

    return {
        "files": found_files,
        "total_count": len(found_files),
        "last_scan": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "syftbox_path": syftbox_path
    }


@register_endpoint("/api/happybird/content")
def get_happybird_content():
    """Get the content of a specific happybird.txt file

    In a real implementation, this would accept a file path parameter
    and return the content of that specific file.
    """

    # For now, return empty content (no file selected by default)
    return {
        "selected_file": None,
        "content": "",
        "error": None
    }


@register_endpoint("/api/happybird/stats")
def get_happybird_stats():
    """Get statistics about happybird.txt files in the system"""

    files_data = get_happybird_files()
    files = files_data.get("files", [])

    # Calculate statistics
    total_size = sum(f.get("size", 0) for f in files)
    owners = list(set(f.get("owner", "unknown") for f in files))

    return {
        "total_files": len(files),
        "total_size_bytes": total_size,
        "unique_owners": len(owners),
        "owners_list": owners,
        "average_size": total_size / len(files) if files else 0,
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
