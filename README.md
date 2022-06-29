# PY-GSTOOLS

Tool classes and functions for Guiosoft projects

[![CodeQL](https://github.com/guionardo/py-gstools/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/guionardo/py-gstools/actions/workflows/codeql-analysis.yml)
[![Upload Python Package](https://github.com/guionardo/py-gstools/actions/workflows/python-publish.yml/badge.svg)](https://github.com/guionardo/py-gstools/actions/workflows/python-publish.yml)
![PyPI](https://img.shields.io/pypi/v/py-gstools)
![PyPI - Downloads](https://img.shields.io/pypi/dm/py-gstools)
[![Pylint](https://github.com/guionardo/py-gstools/actions/workflows/pylint.yml/badge.svg)](https://github.com/guionardo/py-gstools/actions/workflows/pylint.yml)
[![codecov](https://codecov.io/gh/guionardo/py-gstools/branch/develop/graph/badge.svg?token=ErE1TCweih)](https://codecov.io/gh/guionardo/py-gstools)

## Installing

```bash
pip install py-gstools
```
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

## DotEnv

Read environment variables from .env file

(Yeah, I know there is a py-dotenv package, but this is small and better to my needs)

Usage:

```python
import os
from gs.dotenv import load_env

# .env file
# CONFIGURATION_ONE=some_nasty_thing
# LOG_LEVEL=debug

load_env(verbose=True)
```

```bash
2022-06-28 15:59:05,052 INFO load_env(file_name=.env - {'CONFIGURATION_ONE': 'some_nasty_thing', 'LOG_LEVEL': 'debug'})
```

## Config

Configuration classes from files or environment variables

## Read data from environment variables

```python
from gs.config import BaseConfig

class EnvConfig(BaseConfig):
    """Environment based config"""

    TESTING_ALPHA: str = 'alpha'   # ENV:TEST_ALPHA
    TESTING_BETA: str = 'beta'
    TESTING_GAMMA: bool = False     # ENV:TEST_GAMMA

# Here, the environment variables must be available by the OS (by os.environ)

# TESTING_ALPHA field maps to TEST_ALPHA environment var (defined in the comment)
# TESTING_BETA field maps to TESTING_BETA (default behavior, same to field name)
# TESTING_GAMMA fiels maps to TEST_GAMMA

cfg = EnvConfig.load_from_env()

print(cfg.sample_dict())

{'TESTING_BETA': 'beta', 'TEST_ALPHA': 'alpha', 'TEST_GAMMA': False}

```

## Read data from file

config.json file
```json
{
"TESTING_BETA": "beta", 
"TEST_ALPHA": "alpha",
"TEST_GAMMA": true
}
```

config.yaml file
```yaml
TESTING_BETA: beta
TEST_ALPHA: alpha
TEST_GAMMA: true
```

```python
from gs.config import BaseConfig

class EnvConfig(BaseConfig):
    """Environment based config"""

    TESTING_ALPHA: str = 'alpha'   # ENV:TEST_ALPHA
    TESTING_BETA: str = 'beta'
    TESTING_GAMMA: bool = True     # ENV:TEST_GAMMA

cfg = EnvConfig.load_from_file('config.json')

print(cfg.sample_dict())

{'TESTING_BETA': 'beta', 'TEST_ALPHA': 'alpha', 'TEST_GAMMA': True}

```

## Composite configurations

config.json file
```json
{
    "INT_ARG": 2,
    "LIST_ARG": ["1", "2", "3", "4"],
    "STR_ARG": "1234ABCD",
    "SUB_CONFIG": {
        "ARG_1": 10, 
        "ARG_2": "abc"
        },
    "INT_ARG_2": 10,
    "SUB_CONFIGS": [
        {
            "ARG_1": 2, 
            "ARG_2": "EFGH"
        },
        {
            "ARG_1": 3,
            "ARG_2": "IJKL"
        }
    ]
}
```

config.yaml file
```yaml
INT_ARG: 2
INT_ARG_2: 10
LIST_ARG:
- '1'
- '2'
- '3'
- '4'
STR_ARG: 1234ABCD
SUB_CONFIG:
  ARG_1: 10
  ARG_2: ABCD
SUB_CONFIGS:
- ARG_1: 2
  ARG_2: EFGH
- ARG_1: 3
  ARG_2: IJKL
```

```python
from gs.config import BaseConfig

class SubConfig(BaseConfig):
    """Sample configuration class"""
    ARG_1: int = 10
    ARG_2: str = 'abc'


class Config(BaseConfig):
    """Sample configuration class"""

    INT_ARG: int = 1  # DOCUMENT FOR INT_ARG
    INT_ARG_2: int
    STR_ARG = 'abcd'  # DOCUMENT FOR STR_ARG
    LIST_ARG: List[str] = ['a', 'b', 'c', 'd']
    SUB_CONFIG: SubConfig
    SUB_CONFIGS: List[SubConfig]

cfg = EnvConfig.load_from_file('config.json')

print(cfg.to_dict())

{'LIST_ARG': ['1', '2', '3', '4'], 'INT_ARG': 2, 'STR_ARG': '1234ABCD', 'SUB_CONFIG': {'ARG_2': 'abc', 'ARG_1': 2}, 'INT_ARG_2': 10, 'SUB_CONFIGS': [{'ARG_2': 'EFGH', 'ARG_1': 2}, {'ARG_2': 'IJKL', 'ARG_1': 3}]}
```

### After loading validation

```python
from gs.config import BaseConfig

class Config(BaseConfig):
    
    ARG_1: int = 10
    ARG_2: str = 'abc'

    def after_load(self):
        if self.ARG_1 <= 0:
            # Invalid argument
            raise TypeError('ARG_1 must be positive', self.ARG_1)
        if self.ARG_2 == 'ABC':
            # Fixing argument
            self.ARG_2 = 'abc'
        
        # Add anything you need to do/validate after loading

```