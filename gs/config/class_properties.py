"""Class Properties functions"""

import inspect

from typing import Dict, Tuple


def get_fields_default_values(cls) -> Dict[str, any]:
    """Returns dict with fields (key) and default_value"""
    data = {member: default_value
            for member, default_value in inspect.getmembers(cls)
            if not member.startswith('__') and not callable(default_value)}
    return data


def get_types(cls) -> Dict[str, Tuple[type, bool]]:
    """Returns dict with fields (key) and (type, is_list)"""

    annotations = getattr(cls, '__annotations__', {})
    data = {}
    for member, member_type in annotations.items():
        if member_type is list:
            raise TypeError(f'{cls}.{member} must be declared List[type]')
        if getattr(member_type, '_name', 'NONE') == 'List':
            data[member] = (member_type.__args__[0], True)
        else:
            data[member] = (member_type, False)

    return data


def get_comments(cls) -> Dict[str, str]:
    """Returns dict with fields (key) and comment"""
    ret = {}
    # inspect things coming from parent classes
    if not inspect.isclass(cls):
        cls = cls.__class__
    for parent in cls.__bases__:
        if parent != object:
            ret.update(get_comments(parent))

    # get class field names
    fields = set(member for member, default_value in inspect.getmembers(cls)
                 if not member.startswith('__') and not callable(default_value)) | \
        set(member for member, _ in getattr(cls, '__annotations__', {}).items())

    # get all lines
    lines = [line
             for line in inspect.getsourcelines(cls)[0]
             if line.strip() and not '"""' in line and not "'''" in line]
    first_line = lines[1]
    indent_root = lines[1][0:len(first_line)-len(first_line.lstrip())]

    # get lines from root indentation with FIELD definition with comments
    field_lines = [line
                   for line in lines
                   if line.startswith(indent_root) and line[len(indent_root)] != ' '
                   and ('=' in line or ':' in line)
                   and '#' in line
                   ]
    for line in field_lines:
        sep = ':' if ':' in line else '='
        field_name = line.split(sep)[0].strip()

        if field_name not in fields:
            continue

        comment = line.split('#', maxsplit=1)[1].strip()
        ret[field_name] = comment

    # get lines from __init__ with FIELD definition with comments
    for line in inspect.getsourcelines(cls.__init__)[0][1:]:
        line = line.strip()
        if not (line.startswith('self.') and '=' in line and '#' in line):
            continue
        field_name = line[5:].split('=')[0].strip()
        comment = line.split('#')[1].strip()
        ret[field_name] = comment

    return ret


def get_envs(cls) -> Dict[str, str]:
    """Get environment variable definitions for fields"""

    comments = get_comments(cls)
    envs = {}
    for field, comment in comments.items():
        if 'ENV:' in comment:
            env = comment.split('ENV:')[1].strip()
            if env:
                envs[field] = env
    return envs
