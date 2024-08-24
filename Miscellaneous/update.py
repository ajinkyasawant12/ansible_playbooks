import os
import re
import shutil

# Variables for Find and Replace
SNAPSHOT_SEARCH = "SNAPSHOT"
SNAPSHOT_REPLACE = "new_snapshot_value"

BUILD_VERSION_SEARCH = "old_build_version"
BUILD_VERSION_REPLACE = "new_build_version"

STREAM_NAME_SEARCH = "old_stream_name"
STREAM_NAME_REPLACE = "new_stream_name"

# Variables for Creating the Properties File
TEMPLATES_DIR = "ccd_src/bin/templates"
SOURCE_FILE = "mdmce_12.0.12.properties"
TARGET_FILE = f"mdmce_{BUILD_VERSION_REPLACE}.properties"

# Directories to ignore
IGNORE_DIRS = {".metadata", ".jazz"}

def should_ignore(path):
    for ignore_dir in IGNORE_DIRS:
        if ignore_dir in path.split(os.sep):
            return True
    return False

def read_file(file_path):
    encodings = ['utf-8', 'ascii']
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                return file.read()
        except (UnicodeDecodeError, FileNotFoundError):
            continue
    raise Exception(f"Unable to read file {file_path} with available encodings")

def read_file_list(file_list_path):
    try:
        with open(file_list_path, 'r') as file:
            return [line.strip() for line in file if line.strip()]
    except Exception as e:
        print(f"Error reading file list {file_list_path}: {e}")
        return []

def replace_in_file(file_path, search_replace_pairs):
    try:
        content = read_file(file_path)
        original_content = content  # Keep the original content for comparison
        
        for search, replace in search_replace_pairs:
            content = re.sub(search, replace, content)
        
        if content != original_content:  # Only write back if there are changes
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            print(f"Updated {file_path}")
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

def main():
    # Read the list of files for each type of replacement
    snapshot_files = read_file_list('snapshot_files.txt')
    build_version_files = read_file_list('build_version_files.txt')
    stream_name_files = read_file_list('stream_name_files.txt')

    # Perform replacements for SNAPSHOT
    for file_path in snapshot_files:
        replace_in_file(file_path, [(SNAPSHOT_SEARCH, SNAPSHOT_REPLACE)])

    # Perform replacements for BUILD_VERSION
    for file_path in build_version_files:
        replace_in_file(file_path, [(BUILD_VERSION_SEARCH, BUILD_VERSION_REPLACE)])

    # Perform replacements for STREAM_NAME
    for file_path in stream_name_files:
        replace_in_file(file_path, [(STREAM_NAME_SEARCH, STREAM_NAME_REPLACE)])

    # Navigate to the templates directory to create the properties file
    templates_path = os.path.join(os.path.dirname(snapshot_files[0]), TEMPLATES_DIR)
    source_file_path = os.path.join(templates_path, SOURCE_FILE)
    target_file_path = os.path.join(templates_path, TARGET_FILE)

    if os.path.exists(source_file_path):
        shutil.copy(source_file_path, target_file_path)
        print(f"Copied {source_file_path} to {target_file_path}")

        # Additional replacements for TARGET_FILE with hardcoded BUILD_VERSION_SEARCH
        replace_in_file(target_file_path, [
            (STREAM_NAME_SEARCH, STREAM_NAME_REPLACE),
            ("12.0.12", BUILD_VERSION_REPLACE)
        ])
        print(f"Updated {target_file_path} with new stream name and build version")
    else:
        print(f"Source file {source_file_path} does not exist")

if __name__ == "__main__":
    main()