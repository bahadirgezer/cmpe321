import json


class Field:
    def __init__(self, name, type):
        self.name = name
        self.type = type

    @staticmethod
    def init_from_json(field_str: str) -> 'Field':
        field = json.loads(field_str)
        return Field(field['name'], field['type'])

    @staticmethod
    def init_from_dict(field_dict: dict) -> 'Field':
        return Field(field_dict['name'], field_dict['type'])

    def to_json(self):
        return json.dumps(self.__dict__)


class Record:
    def __init__(self, primary_key: str, fields: list[str]):
        self.primary_key = primary_key  # primary_key
        self.fields = fields  # field values

    @staticmethod
    def init_from_json(**kwargs) -> 'Record':
        primary_key = kwargs['header']['key']
        fields = kwargs['fields']
        return Record(primary_key, fields)

    def to_json(self) -> dict:
        return {"header": {"key": self.primary_key}, "fields": self.fields}

    def __str__(self):
        return ' '.join(self.fields)


class Page:
    def __init__(self, records: list, page_number, max_records):
        self.page_number = page_number
        self.max_records= max_records
        self.records: list[Record] = records

    @staticmethod
    def init_from_json(**kwargs) -> 'Page':
        header = kwargs['header'][0]
        page_number = header['page_number']
        max_records = header['max_records']
        records = kwargs['records']
        return Page([Record.init_from_json(**record) for record in records], page_number, max_records)

    def to_json(self) -> dict:
        header = {'page_number': self.page_number,
                  'max_records': self.max_records,
                  'num_records': len(self.records)}
        return {"header": [header], "records": [record.to_json() for record in self.records]}

    def __str__(self):
        return f'Page {self.page_number}: {self.records}'


class File:
    """
    File
    header object
    page object: {header + records}
    """

    def __init__(self, type_name: str, pages: list[Page], fields: list[Field], primary_key_field: str, num_pages: int = None):
        self.type_name: str = type_name
        self.fields: list[Field] = fields
        self.primary_key_field: str = primary_key_field
        self.num_pages: int = num_pages if num_pages is not None else len(pages)
        self.pages: list[Page] = pages

    @staticmethod
    def init_from_json(**kwargs) -> 'File':
        type_name = kwargs['type_name']
        fields = [Field.init_from_json(field_str) for field_str in kwargs['fields']]
        primary_key_field = kwargs['primary_key_field']
        num_pages = int(kwargs['num_pages'])
        return File(type_name, [] * int(num_pages), fields, primary_key_field, num_pages)

    def to_json_list(self) -> list[dict]:
        header = {'type_name': self.type_name,
                  'num_fields': len(self.fields),
                  'num_pages': self.num_pages,
                  'primary_key_field': self.primary_key_field,
                  'fields': [field.to_json() for field in self.fields]}
        return [header] + [page.to_json() for page in self.pages]
