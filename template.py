import os
from pathlib import Path
import logging

# Configure logging to display INFO level messages
logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')

# List of files to be created or checked
list_of_files = [
    "src/__init__.py",
    "src/helper.py",
    "src/prompt.py",
    ".env",
    "setup.py",
    "research/trials.ipynb",
    "app.py",
    "store_index.py",
    "static/.gitkeep",
    "templates/chat.html"
]

# Iterate over each file path in the list
for filepath in list_of_files:
    filepath = Path(filepath)  # Convert the file path to a Path object for easier manipulation
    filedir, filename = os.path.split(filepath)  # Separate the directory path and the file name

    # If the directory is not empty (i.e., it's not the current directory)
    if filedir != "":
        # Create the directory if it doesn't exist already
        os.makedirs(filedir, exist_ok=True)
        # Log a message indicating the directory creation for the corresponding file
        logging.info(f"Creating directory; {filedir} for the file {filename}")

    # Check if the file doesn't exist or is empty
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        # Create an empty file
        with open(filepath, 'w') as f:
            pass  # Do nothing (create an empty file)
        # Log a message indicating the creation of the empty file
        logging.info(f"Creating empty file: {filepath}")

    else:
        # Log a message indicating that the file already exists
        logging.info(f"{filename} is already created")
