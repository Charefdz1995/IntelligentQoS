from mongoengine import *

interface_type_choices = ("FastEthernet","Ethernet", "GigaEthernet", "Serial")

class interface(DynamicDocument):
        interface_type = StringField(required=True, choices = interface_type_choices)
        interface_shelf = IntField(required=False)
        interface_slot = IntField(required=True)
        interface_port = IntField(required=True)
        interface_address = StringField(required=False)
        interface_mask = StringField(required=False)
        ingress = BooleanField(default = False)

        @property
        def interface_name(self):
                if self.interface_shelf == None:
                        return '%s %s/%s' %(self.interface_type,self.interface_slot,
                                        self.interface_port)
                else:
                        return '%s %s/%s/%s' %(self.interface_type,self.interface_shelf,
                                                self.interface_slot,self.interface_port)
        meta = {'abstract': True}

class access(DynamicEmbeddedDocument):
        management_address = StringField(required=True)
        username = StringField(required=True)
        password = StringField(required=True)
        enable_secret = StringField(required=True)

class device(DynamicDocument):
        hostname = StringField(required=True)
        management = EmbeddedDocumentField(access)
        interfaces = ListField(ReferenceField(interface))
        loopback_addr = StringField()
        meta = {'abstract': True}

class link(DynamicDocument):
        from_switch = ReferenceField(device)
        from_interface =  ReferenceField(interface)
        to_switch = ReferenceField(device)
        to_interface = ReferenceField(interface)

        meta = {'abstract': True}

class topology(DynamicDocument):
        topology_name = StringField(required=True)
        devices = ListField(ReferenceField(device))
        links = ListField(ReferenceField(link))
        meta = {'abstract' : True}