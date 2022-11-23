import os
import sys
import time
import threading
import subprocess
from smart_open import open

from omniparser.utils import read_line
from omniparser.constants import OP_BIN_PATH, SCHEMA_MAP


class OmniParser(object):

    def __init__(self, schema: str) -> None:
        if not SCHEMA_MAP.get(schema):
            ValueError("Could not find the schema")
        package_path = os.path.dirname(os.path.abspath(__file__))
        self._schema_file_path = os.path.join(package_path, SCHEMA_MAP.get(schema))
        self._bin_path = os.path.join(package_path, OP_BIN_PATH)

    def transform(self, input_file_path: str, dest_file_path: str) -> None:
        dest_file = open(dest_file_path, 'w')
        parser = subprocess.Popen([self._bin_path, "transform", "-s", f"{self._schema_file_path}"],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    universal_newlines=True,
                    bufsize=0,
                    close_fds=True,
                )
        t = threading.Thread(target=self._capture_output, args=(parser, dest_file,))
        t.start()
        with read_line(input_file_path) as lines:
            for line in lines:
                parser.stdin.write(line)
                # print(f'input - {time.strftime("%Y-%m-%d %H:%M:%S")} - {line}')
                time.sleep(.1)
        parser.stdin.close()
        parser.wait()
        t.join()
        dest_file.close()

    def _capture_output(self, popen: subprocess.Popen, dest_file):
        for line in popen.stdout:
            # print(f'output - {time.strftime("%Y-%m-%d %H:%M:%S")} - {line}')
            dest_file.write(line)
            dest_file.flush()
            sys.stdout.flush()


if __name__ == "__main__":
    pass
