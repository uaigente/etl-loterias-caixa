from frictionless import Package
from pathlib import Path
import tempfile
import subprocess

package = Package('datapackage.yaml')
resource = package.get_resource('mega_sena')
df = resource.to_pandas()
print(df)
