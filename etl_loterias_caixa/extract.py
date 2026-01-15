import logging

import requests
from frictionless import Package

from helpers import normalize_excel_with_libreoffice
from pathlib import Path

logger = logging.getLogger(__name__)


def extract_resource(resource):
    """
    Extract a isolated resource from a datapackage.
    """
    try:
        sources = resource.sources
        sources = [
            source for source in sources if source.get('method') is not None
        ]
        source = sources[0]
        if source:
            logger.info(f'Extracting resource {resource.name}.')
            func = getattr(requests, source['method'])
            # TODO: Pass parameters as **kwargs
            response = func(
                source['path'],
                timeout=source['timeout'] if 'timeout' in source else 30,
                params=source['params'] if 'params' in source else {},
            )
            response.raise_for_status()

        with open(resource.path, 'wb') as f:
            f.write(response.content)

        logger.info(f'CSV file successfully downloaded to: {resource.path}.')
        logger.info(f'File size: {len(response.content):,} bytes.')

    except requests.exceptions.RequestException as e:
        print(f'Error downloading file: {e}')
        raise
    except IOError as e:
        print(f'Error saving file: {e}')
        raise


def extract_resources(descriptor: str = 'datapackage.yaml'):
    """
    Extract resources from a datapackage.
    """
    logger.info(f'Extracting resources from {descriptor}.')
    package = Package(descriptor)

    for resource in package.resources:
        extract_resource(resource)
        if resource.to_pandas().empty:
            logger.warning(
                f'Dataframe {resource.name} is empty after extraction.')
            normalize_excel_with_libreoffice(Path(resource.path))


if __name__ == '__main__':
    extract_resources()
