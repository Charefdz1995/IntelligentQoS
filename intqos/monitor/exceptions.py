class Error(Exception):
	pass 

class NotExistingDestination(Error):
	print("NetFlow destination collector address is required")


class NotDefinedParameter(Error):
	print("One parameter is not defined")

