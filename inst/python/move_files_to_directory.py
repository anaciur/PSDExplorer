import os
import shutil

# Utility to add .tsv extension
def add_tsv_extension(original_list):
    return [item + '.tsv' for item in original_list]


# --- Dynamic path setup ---
BASE_DIR = os.path.dirname(__file__)
file_extension = ".tsv"


def move_files_with_extension(source_dir, destination_dir, extension, files_to_move):
    """Move a specific list of files from source_dir to destination_dir."""
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)
    for file_name in files_to_move:
        source_path = os.path.join(source_dir, file_name)
        destination_path = os.path.join(destination_dir, file_name)
        if os.path.exists(source_path):
            shutil.move(source_path, destination_path)
            print(f"Moved: {file_name}")
        else:
            print(f"⚠️ Skipped missing file: {file_name}")


# --- NOTE ---
# Previously this script executed automatically at import (causing FileNotFoundError).
# All automatic code execution is now disabled.
# This module only defines helper functions and constants for use by other scripts.
# Nothing runs on import anymore.
