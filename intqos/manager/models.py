from django.db import models

# Create your models here.
from mongoengine import * 
from common.models import * 
from jinja2 import Environment, FileSystemLoader
from intqos.settings import NET_CONF_TEMPLATES

zone_type = (('Egress', 'Egress'),('Ingress', 'Ingress'))
match_type =('match-any','match-all')

class interface(interface_base):
	zone_type = StringField(max_length=6, choices=zone_type)

class classification_class(EmbeddedDocument):
	name = StringField(required=True)
	match_type = StringField(choices=match_type)
	matches = ListField(StringField())
	dscp_value = StringField()
	priorty = StringField()
	drop_prob = StringField()
class policyIn(EmbeddedDocument):
	name = StringField(required=True)
	classes = ListField(EmbeddedDocumentField(classification_class))
class policyOut(EmbeddedDocument):
	name = StringField(required=True)
	classes = ListField(EmbeddedDocumentField(classification_class))
class switch(switch):
	zone_type = StringField(max_length=6, choices=zone_type)
	policyIn = EmbeddedDocumentField(policyIn)
	policyOut = EmbeddedDocumentField(policyOut)
	def baseline(self):
		env = Environment(loader = FileSystemLoader(NET_CONF_TEMPLATES))
		template = env.get_template("baseline.j2")
		output = template.render(self = self)
