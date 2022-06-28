"""Base Configuration module"""

import json
import os
from datetime import date, datetime, timedelta

import yaml

from .class_properties import get_envs, get_fields_default_values, get_types


def _create_config_field(internal_name: str, field_type: type,
                         is_list: bool, default_value: any, field_name: str):
    if not field_type:
        if default_value is None:
            raise ValueError(f'No type specified for {internal_name}')
        field_type = type(default_value)
    if default_value is None:
        default_value = field_type()
    if not field_name:
        field_name = internal_name

    def __parse_value_type(value, value_type):
        if value_type in (int, float, bool, str):
            return value_type(value)

        if value_type == datetime:
            return datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        if value_type == date:
            return date.strptime(value, '%Y-%m-%d')
        if value_type == timedelta:
            return timedelta(**value)
        if issubclass(value_type, BaseConfig):
            return value_type(value)
        if isinstance(value_type, list):
            return [__parse_value_type(v, value_type[0]) for v in value]

        raise TypeError(f'Unknown type {value_type}')

    def load(source: dict) -> any:
        if field_name in source:
            source_value = source[field_name]
            if not is_list:
                source_value = __parse_value_type(source_value, field_type)
            else:
                source_value = [__parse_value_type(v, field_type)
                                for v in source_value]
        else:
            source_value = default_value

        return source_value

    return load


class BaseConfig:
    """Base Configuration class

    Field types:
    - int
    - float
    - bool
    - str
    - datetime.datetime
    - datetime.date
    - datetime.timedelta
    - BaseConfig inherited classes
    - list (of types above)
    """

    def __init__(self, source=None, **dict_source):
        self.__fields = self.__parse_fields()
        self.__load(source or dict_source)

    def __parse_fields(self):

        default_values = get_fields_default_values(self)
        types = get_types(self)
        envs = get_envs(self)

        all_field_names = set(default_values.keys()) | set(types.keys())

        data = {
            field: _create_config_field(field,
                                        *types.get(field, (None, False)),
                                        default_values.get(field, None),
                                        envs.get(field, field))

            for field in all_field_names
        }

        return data

    def __load(self, source):
        if source is None:
            return

        if isinstance(source, str):
            if os.path.isfile(source):
                source = self.__parse_file(source)
            else:
                source = self.__parse_content(source)

        if not isinstance(source, dict):
            return

        for member, field in self.__fields.items():
            setattr(self, member, field(source))

    def __parse_value_type(self, value_type, value):
        if value_type in (int, float, bool, str):
            return value_type(value)

        if value_type == datetime:
            return datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        if value_type == date:
            return date.strptime(value, '%Y-%m-%d')
        if value_type == timedelta:
            return timedelta(**value)
        if issubclass(value_type, BaseConfig):
            return value_type(value)
        if isinstance(value_type, list):
            return [self.__parse_value_type(value_type[0], v) for v in value]

        raise TypeError(f'Unknown type {value_type}')

    def __parse_file(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as file:
                content = file.read()
        except Exception as exc:
            raise ValueError(f'Error reading file {path}: {exc}') from exc

        return self.__parse_content(content)

    def __parse_content(self, content):
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            # Pass to yaml parser
            ...
        except Exception as exc:
            raise ValueError(f'Error parsing content {exc}') from exc
        try:
            return yaml.load(content, yaml.SafeLoader)
        except Exception as exc:
            raise ValueError(f'Error parsing content {exc}') from exc

    def __repr__(self) -> str:
        fields = ", ".join(
            f"{k}={repr(getattr(self,k))}" for k in self.__fields)
        return f'{self.__class__.__name__}({fields})'

    def __dict__(self) -> dict:
        return
