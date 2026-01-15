from frictionless import Package

# package = Package('datapackage_csv.yaml')
# resource = package.get_resource('mega_sena')
# df = resource.to_pandas()

package = Package('datapackage.yaml')
resource = package.get_resource('mega_sena')
df = resource.to_pandas()
print(df.head())
