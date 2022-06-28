# PY-GSTOOLS

Tool classes and functions for Guiosoft projects

[![CodeQL](https://github.com/guionardo/py-gstools/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/guionardo/py-gstools/actions/workflows/codeql-analysis.yml)
[![Upload Python Package](https://github.com/guionardo/py-gstools/actions/workflows/python-publish.yml/badge.svg)](https://github.com/guionardo/py-gstools/actions/workflows/python-publish.yml)
![PyPI](https://img.shields.io/pypi/v/py-gstools)
![PyPI - Downloads](https://img.shields.io/pypi/dm/py-gstools)
[![Pylint](https://github.com/guionardo/py-gstools/actions/workflows/pylint.yml/badge.svg)](https://github.com/guionardo/py-gstools/actions/workflows/pylint.yml)

## Cache

Cache wrapper for multiple providers.

Usage:

```python
from datetime import timedelta
from gs.cache import get_cache

cache = get_cache('memory')

#    connection string can be:
#    - memory
#    - path:/path/to/cache/directory
#    - redis://host:port/db_number

cache.set(key='key',
          value='This is an cached data', 
          ttl=timedelta(seconds=600))

value = cache.get('key')

print(value)
```