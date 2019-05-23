from mongoengine import * 



class interface(EmbededDocument):
	interface_type = StringField(required=True)
	interface_shelf = intField(required=False)
	interface_slot = intField(required=True)
	interface_port = intField(required=True)
	interface_name = StringField(required=True)

class access(EmbededDocument):
	management_address = StringField(required=True)
	username = StringField(required=True)
	password = StringField(required=True)
	enable_secret = StringField(required=True)

class switch(EmbededDocument):
	hostname = StringField(required=True)
	management = EmbededDocumentField(access)
	interfaces = listField(EmbededDocumentField(interface))

class link_side(EmbededDocument):
	switch = ReferenceField(switch)
	interface = ReferenceField(interface)

class link(EmbededDocument):
	link_description = StringField(required=False)
	from_interface =  EmbededDocumentField(link_side)
	to_interface = EmbededDocumentField(link_side)

class topology(Document):
	topology_name = StringField(required=True)
	switches = listField(EmbededDocumentField(switch))
	links = listField(EmbededDocumentField(link))