import logging
import os

logger = logging.getLogger('gs.dotenv')


def load_env(file_name: str = '.env', extra_source: dict = None, verbose: bool = False) -> bool:
    """Load environment variables from a file or dict."""
    if not isinstance(extra_source, dict):
        extra_source = {}
    if extra_source:
        if verbose:
            logger.info(f'load_env(extra_source={extra_source})')
        os.environ.update(extra_source)
        return True

    try:
        with open(file_name) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#') or '=' not in line:
                    continue
                key, value = line.split('=', 1)
                extra_source[key.strip()] = value.strip()
        if not extra_source:
            if verbose:
                logger.info(f'load_env(file_name={file_name}) - no data')
        else:
            if verbose:
                logger.info(
                    f'load_env(file_name={file_name}) - {extra_source}')
            os.environ.update(extra_source)
        return True
    except Exception as exc:
        logger.error(f'load_env(file_name={file_name}) - error: {exc}')

    return False
