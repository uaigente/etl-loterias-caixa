from frictionless import Package
import logging
from pipelines import transform_pipeline

logger = logging.getLogger(__name__)

def transform_resource(resource):
    """
    Transform a isolated resource from a datapackage.
    """
    logger.info(f'Transforming resource {resource.name}')

    df = resource.to_pandas()
    for field in resource.schema.fields:
        target = field.custom.get('target')
        target = target if target else field.name.replace(' ', '_').lower()
        df.rename(columns={field.name: target}, inplace=True)

    df.to_csv(f'data/{resource.name}.csv',
              index=False,
              sep=',',
              encoding='utf-8',
    )

def transform_resources(descriptor: str = 'datapackage.yaml'):
    """
    Transform resources from a datapackage.
    """
    logger.info(f'Extracting resources from {descriptor}.')
    package = Package(descriptor)

    for resource in package.resources:
        transform_resource(resource)

if __name__ == '__main__':
    transform_resources()
