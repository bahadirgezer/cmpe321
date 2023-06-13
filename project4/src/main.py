import os
import sys
import data.operations as operations
import time as t
from data.structure import Record


if __name__ == '__main__':
    print("current working directory: ", os.getcwd())
    # if cwd does not end with 'src', change to 'src'
    if not os.getcwd().endswith('src'):
        try:
            os.chdir('src')
        except OSError:
            print("Can't change the Current Working Directory")
            exit(1)

    if len(sys.argv) != 3:
        print('Usage: python3 main.py <input-file-path> <output-file-path>')
        sys.exit(1)

    input_file_path, output_file_path = sys.argv[1], sys.argv[2]

    try:
        with open(input_file_path) as f:
            input_lines = f.readlines()
            if len(input_lines) == 0:
                print(f'File is empty: {input_file_path}')
                sys.exit(1)
    except FileNotFoundError:
        print(f'File not found: {input_file_path}')
        sys.exit(1)

    # iterate through input lines
    input_lines = [line.split() for line in input_lines]
    output_lines = []
    log_lines = []
    for line in input_lines:

        # create record <type-name><field1-value><field2-value>...
        if line[0] == 'create' and line[1] == 'record':
            result = operations.create_record(line[2], line[3:])
            log_line = str(int(t.time())) + ', ' + ' '.join(line) + ', ' + ('success' if result else 'failure') + '\n'
            log_lines.append(log_line)

        # delete record <type-name><primary-key>
        elif line[0] == 'delete' and line[1] == 'record':
            result = operations.delete_record(line[2], line[3])
            log_line = str(int(t.time())) + ', ' + ' '.join(line) + ', ' + (' success' if result else ' failure') + '\n'

        # search record <type-name><primary-key>
        elif line[0] == 'search' and line[1] == 'record':
            record = operations.search_record(line[2], line[3])
            log_line = str(int(t.time())) + ', ' + ' '.join(line) + ', ' + (' success' if record else ' failure') + '\n'
            output_lines.append(str(record) + '\n')

        # create type <type-name><number-of-fields><primary-key-order><field1-name><field1-type><field2-name>...
        elif line[0] == 'create' and line[1] == 'type':
            result = operations.create_type(line[2], int(line[3]), int(line[4]), line[5::2], line[6::2])
            log_line = str(int(t.time())) + ', ' + ' '.join(line) + ', ' + (' success' if result else ' failure') + '\n'

        else:
            print(f'Invalid input: {line}')

    # write output file with exception handling
    try:
        with open(output_file_path, 'w') as f:
            f.writelines(output_lines)
    except FileNotFoundError:
        # create file if it doesn't exist
        with open(output_file_path, 'x') as f:
            f.writelines(output_lines)
    except PermissionError:
        print(f'Permission denied: {output_file_path}')
        sys.exit(1)

    # write log file with exception handling
    # int(time.time()), log_line, (sucesss | failure)
    try:
        with open('../westerosLog.csv', 'a') as f:
            f.writelines(log_lines)
    except FileNotFoundError:
        # create file if it doesn't exist
        with open('../westerosLog.csv', 'x') as f:
            f.writelines(log_lines)
    except PermissionError:
        print(f'Permission denied: {output_file_path}')
        sys.exit(1)

    sys.exit(0)

from data.structure import Record
