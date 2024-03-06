#!/usr/bin/python3
"""__init__.py for model directory"""

from models.engine.file_storage import FileStorage

storage = FileStorage()
storage.reload()
