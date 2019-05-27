from mongoengine import * 



class interface_base(DynamicEmbeddedDocument):
	interface_type = StringField(required=True)
	interface_shelf = IntField(required=False)
	interface_slot = IntField(required=True)
	interface_port = IntField(required=True)

	@property
	def interface_name(self):
		if self.interface_shelf == None:
			return '%s %s/%s' %(self.interface_type,self.interface_slot,self.interface_port)
		else:
			return '%s %s/%s/%s' %(self.interface_type,self.interface_shelf,self.interface_slot,self.interface_port)


	meta = {'allow_inheritance': True}

class access(DynamicEmbeddedDocument):
	management_address = StringField(required=True)
	username = StringField(required=True)
	password = StringField(required=True)
	enable_secret = StringField(required=True)

	meta = {'allow_inheritance': True}

class switch(DynamicEmbeddedDocument):
	hostname = StringField(required=True)
	management = EmbededDocumentField(access)
	interfaces = ListField(EmbededDocumentField(interface_base))

	meta = {'allow_inheritance': True}



class link_side(DynamicEmbeddedDocument):
	switch = ReferenceField(switch)
	interface = ReferenceField(interface)

	meta = {'allow_inheritance': True}

class link(DynamicEmbeddedDocument):
	link_description = StringField(required=False)
	from_interface =  EmbededDocumentField(link_side)
	to_interface = EmbededDocumentField(link_side)

	meta = {'allow_inheritance': True}

class topology(DynamicDocument):
	topology_name = StringField(required=True)
	switches = ListField(EmbededDocumentField(switch))
	links = ListField(EmbededDocumentField(link))

	meta = {'allow_inheritance': True}
