import yaml


class YAMLSerializer:
	"""
	class for serialization YAML
	"""
	def serialize(self, obj, file):
		"""
		Encode obj to yaml format and write it into file.
		"""
		yaml.dump(obj.notes, file)

	def deserialize(self, file):
		"""
		Decode from file to Python-object using yaml.
		"""
		return yaml.load(file)
