import os
import tempfile
import io


class FileAccessWrapper:
    def __init__(self, filename):
        self.filename = filename

    def open(self):
        return open(self.filename, "w+", encoding="UTF-8")


class FileOpen:
    def __init__(self, file_access):
        self.file_access = file_access
        with self.file_access.open() as f:
            pass

    def get_item(self):
        return "vijay"



filename = os.path.join(tempfile.gettempdir(), "aflie.txt")
FileOpen(FileAccessWrapper(filename))

