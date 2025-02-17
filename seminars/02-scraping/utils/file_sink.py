import json

class FileSink:
    def __init__(self, path):
        self._file = open(path, 'w')

    def write(self, item):
        self._file.write(json.dumps(item, ensure_ascii=False) + '\n')

    def __del__(self):
        self._file.close()
