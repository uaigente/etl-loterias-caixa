from frictionless import Package

package = Package('datapackage.yaml')
resource = package.get_resource('mega_sena')
df = resource.to_pandas()
print(df)
