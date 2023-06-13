import json

# newline JSON, or ndjson, is a JSON file where each line is a JSON object.
# This is useful for streaming large JSON files.

# The following code will read a newline JSON file and print each line.


class NewlineJsonReader:
    def __init__(self, file):
        self.file = file
        self.open_file = None

    def read(self) -> list[dict]:
        with open(self.file) as f:
            for line in f:
                yield json.loads(line)

    def read_first(self) -> dict:
        with open(self.file) as f:
            return json.loads(f.readline())

    def read_rest(self) -> list[dict]:
        with open(self.file) as f:
            return [json.loads(line) for line in f.readlines()[1:]]

    def start_rest_read(self) -> None:
        self.open_file = open(self.file)
        self.open_file.readline()

    def reset_rest_read(self) -> None:
        self.open_file.close()
        self.open_file = open(self.file)

    def close_rest_read(self) -> None:
        self.open_file.close()

    def read_rest_line(self) -> dict:
        return json.loads(self.open_file.readline())


class NewlineJsonWriter:
    def __init__(self, file):
        self.file = file

    def write(self, data: list[dict]):
        with open(self.file, 'w') as f:
            for line in data:
                f.write(json.dumps(line) + '\n')

    def write_first(self, data: dict):
        # only write the first line
        # keep the rest of the file
        with open(self.file, 'r') as f:
            lines = f.readlines()
        with open(self.file, 'w') as f:
            f.write(json.dumps(data) + '\n')
            f.writelines(lines[1:])

    def append(self, data: dict):
        with open(self.file, 'a') as f:
            f.write(json.dumps(data) + '\n')

    def append_rest(self, data: list[dict]):
        with open(self.file, 'a') as f:
            for line in data:
                f.write(json.dumps(line) + '\n')

    def write_line(self, data: dict, line: int):
        with open(self.file, 'r') as f:
            lines = f.readlines()
        with open(self.file, 'w') as f:
            lines[line] = json.dumps(data) + '\n'
            f.writelines(lines)
