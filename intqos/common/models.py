from mongoengine import *


connect('exdb',host = '0.0.0.0',port = 27017)



class interface_base(DynamicDocument):
        interface_type = StringField(required=True)
        interface_shelf = IntField(required=False)
        interface_slot = IntField(required=True)
        interface_port = IntField(required=True)
        interface_address = StringField(required=False)
        interface_mask = StringField(required=False)

        @property
        def interface_name(self):
                if self.interface_shelf == None:
                        return '%s %s/%s' %(self.interface_type,self.interface_slot,
                                        self.interface_port)
                else:
                        return '%s %s/%s/%s' %(self.interface_type,self.interface_shelf,
                                                self.interface_slot,self.interface_port)


        meta = {'allow_inheritance': True}

class access(DynamicEmbeddedDocument):
        management_address = StringField(required=True)
        username = StringField(required=True)
        password = StringField(required=True)
        enable_secret = StringField(required=True)

        meta = {'allow_inheritance': True}

class switch(DynamicDocument):
        hostname = StringField(required=True)
        management = EmbeddedDocumentField(access)
        interfaces = ListField(ReferenceField(interface_base))

        meta = {'allow_inheritance': True}





class link(DynamicDocument):
        from_switch = ReferenceField(switch)
        from_interface =  ReferenceField(interface_base)
        to_switch = ReferenceField(switch)
        to_interface = ReferenceField(interface_base)

        meta = {'allow_inheritance': True}

class topology(DynamicDocument):
        topology_name = StringField(required=True)
        switches = ListField(ReferenceField(switch))
        links = ListField(ReferenceField(link))
