import json
import os
import data.structure as structure
import data.newlineJson as nlj
from data.structure import Record


def create_record(type_name: str, field_values: list[str]) -> bool:
    if not os.path.exists(f'../data/{type_name}.ndjson'):
        print(f'Type does not exist: {type_name}')
        return False

    # read header
    file_reader = nlj.NewlineJsonReader(f'../data/{type_name}.ndjson')
    header = file_reader.read_first()
    file = structure.File.init_from_json(**header)

    if len(field_values) != len(file.fields):
        print(f'Invalid number of fields: {len(field_values)}')
        return False

    # find index of primary key field
    primary_key_index = -1
    for i in range(len(file.fields)):
        if file.fields[i].name == file.primary_key_field:
            primary_key_index = i
            break

    # create record
    primary_key = field_values[primary_key_index]
    record = structure.Record(primary_key, field_values)

    # check if record already exists
    file_reader.start_rest_read()
    for i in range(file.num_pages):
        page = file_reader.read_rest_line()
        page_object = structure.Page.init_from_json(**page)
        for record in page_object.records:
            if record.primary_key == primary_key:
                print(f'Record already exists: {record}')
                return False
    file_reader.close_rest_read()

    # find page to add record to
    page_index = -1
    file_reader.start_rest_read()
    record_page = None
    for i in range(file.num_pages):
        page = file_reader.read_rest_line()
        print(page)
        page_object = structure.Page.init_from_json(**page)
        if len(page_object.records) < page_object.max_records:
            page_index = i
            record_page = structure.Page.init_from_json(**page)
            break
    file_reader.close_rest_read()

    if page_index == -1:
        # create new page
        page_index = file.num_pages
        record_page = structure.Page([], page_index, 10)
        file.num_pages += 1
        file.pages = [] * file.num_pages
        file.pages.append(record_page)

    # add record to page
    record_page.records.append(record)

    # write to file
    file_writer = nlj.NewlineJsonWriter(f'../data/{type_name}.ndjson')
    file_writer.write_first(file.to_json_list()[0])
    file_writer.write_line(record_page.to_json(), page_index + 1)


def delete_record(type_name: str, primary_key: str) -> bool:
    if not os.path.exists(f'../data/{type_name}.ndjson'):
        print(f'Type does not exist: {type_name}')
        return False

    # read header
    file_reader = nlj.NewlineJsonReader(f'../data/{type_name}.ndjson')
    header = file_reader.read_first()
    file = structure.File.init_from_json(**header)

    # search for record
    page = {}
    page_index = -1
    record_index = -1
    file_reader.start_rest_read()
    for i in range(file.num_pages):
        page = file_reader.read_rest_line()
        page_obj = structure.Page.init_from_json(**page)
        for j in range(len(page_obj.records)):
            record = page_obj.records[j]
            if record.primary_key == primary_key:
                page_index = i
                record_index = j
                break
        if page_index != -1:
            break
    file_reader.close_rest_read()
    if page_index == -1:
        print(f'Record not found: {primary_key}')
        return False

    # delete record
    page_obj = structure.Page.init_from_json(**page)
    page_obj.records.pop(record_index)

    # write to file
    file_writer = nlj.NewlineJsonWriter(f'../data/{type_name}.ndjson')
    file_writer.write_line(page_obj.to_json(), page_index + 1)


def search_record(type_name: str, primary_key: str) -> Record | bool:
    if not os.path.exists(f'../data/{type_name}.ndjson'):
        print(f'Type does not exist: {type_name}')
        return False

    # read header
    file_reader = nlj.NewlineJsonReader(f'../data/{type_name}.ndjson')
    header = file_reader.read_first()
    file = structure.File.init_from_json(**header)

    # search for record
    page = {}
    page_index = -1
    record_index = -1
    file_reader.start_rest_read()
    for i in range(file.num_pages):
        page = file_reader.read_rest_line()
        page_obj = structure.Page.init_from_json(**page)
        for j in range(len(page_obj.records)):
            record = page_obj.records[j]
            if record.primary_key == primary_key:
                page_index = i
                record_index = j
                break
        if page_index != -1:
            break
    file_reader.close_rest_read()
    if page_index == -1:
        print(f'Record not found: {primary_key}')
        return False

    # return record
    record_json = page['records'][record_index]
    record_json = json.loads(record_json)
    record = structure.Record.init_from_json(record_json['fields'])
    return record


def create_type(type_name: str, number_of_fields: int, primary_key_order: int, field_names: list[str], field_types: list[str]):
    if len(field_names) != len(field_types):
        print(f'Invalid input: {field_names} {field_types}')
        return False

    if primary_key_order < 1 or primary_key_order > len(field_names):
        print(f'Invalid primary key order: {primary_key_order}')
        return False

    if number_of_fields != len(field_names):
        print(f'Invalid number of fields: {number_of_fields}')
        return False

    # check if type already exists
    if os.path.exists(f'../data/{type_name}.ndjson'):
        print(f'Type already exists: {type_name}')
        return False

    # create type
    primary_key_field: str = field_names[primary_key_order - 1]
    fields: list[structure.Field] = [structure.Field(field_names[i], field_types[i]) for i in range(len(field_names))]
    pages: list[structure.Page] = [structure.Page([], 1, 10)]
    file: structure.File = structure.File(type_name, pages, fields, primary_key_field)

    # save type to file
    file_writer = nlj.NewlineJsonWriter(f'../data/{type_name}.ndjson')
    file_writer.write(file.to_json_list())

    # create index file
    index_file_writer = nlj.NewlineJsonWriter(f'../data/index/{type_name}.ndjson')
    index_file_writer.write([])
