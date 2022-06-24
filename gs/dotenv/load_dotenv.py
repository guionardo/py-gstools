"""Dotenv functions"""
import logging
import os

logger = logging.getLogger('gs.dotenv')


def load_env(file_name: str = '.env', extra_source: dict = None, verbose: bool = False) -> bool:
    """Load environment variables from a file or dict."""
    if not isinstance(extra_source, dict):
        extra_source = {}
    if extra_source:
        if verbose:
            logger.info('load_env(extra_source=%s)', extra_source)
        os.environ.update(extra_source)
        return True

    try:
        with open(file_name, encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith('#') or '=' not in line:
                    continue
                key, value = line.split('=', 1)
                extra_source[key.strip()] = value.strip()
        if not extra_source:
            if verbose:
                logger.info('load_env(file_name=%s) - no data', file_name)
        else:
            if verbose:
                logger.info('load_env(file_name=%s - %s)',
                            file_name, extra_source)
            os.environ.update(extra_source)
        return True
    except Exception as exc:
        logger.error('load_env(file_name=%s) - error: %s', file_name, exc)

    return False
