import os
import time
from datetime import datetime
import json
from pathlib import Path

class FileHistoryTracker:
    def __init__(self, history_file="file_history.txt"):
        self.history_file = history_file
        self.history = self._load_history()

    def _load_history(self):
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {}
        return {}

    def _save_history(self):
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f, indent=2)

    def track_files(self, directory="."):
        """Track all files in the given directory and its subdirectories."""
        for root, dirs, files in os.walk(directory):
            # Skip directories that start with a period
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            for file in files:
                # Skip files that start with a period or the history file itself
                if file.startswith('.') or file == self.history_file:
                    continue
                
                file_path = os.path.join(root, file)
                try:
                    mtime = os.path.getmtime(file_path)
                    if file_path not in self.history:
                        self.history[file_path] = []
                    
                    # Check if the file has been modified
                    last_entry = self.history[file_path][-1] if self.history[file_path] else None
                    if not last_entry or last_entry['timestamp'] != mtime:
                        self.history[file_path].append({
                            'timestamp': mtime,
                            'datetime': datetime.fromtimestamp(mtime).isoformat(),
                            'size': os.path.getsize(file_path)
                        })
                except (OSError, FileNotFoundError) as e:
                    print(f"Error tracking {file_path}: {e}")

        self._save_history()

    def get_file_history(self, file_path):
        """Get the history of a specific file."""
        return self.history.get(file_path, [])

    def print_history(self):
        """Print the entire file history in a readable format."""
        for file_path, history in self.history.items():
            print(f"\nFile: {file_path}")
            for entry in history:
                print(f"  Modified: {entry['datetime']}")
                print(f"  Size: {entry['size']} bytes")
                print("  " + "-"*40)

if __name__ == "__main__":
    tracker = FileHistoryTracker()
    tracker.track_files()
    tracker.print_history() 