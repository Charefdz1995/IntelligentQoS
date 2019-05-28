from django.db import models

# Create your models here.
from mongoengine import *
from common.models import *
from jinja2 import Environment, FileSystemLoader
from intqos.settings import NET_CONF_TEMPLATES

zone_type = (('Egress', 'Egress'),('Ingress', 'Ingress'))
match_type =('match-any','match-all')
priorty =('high','priority','normal','low')

class interface(interface_base):
	zone_type = StringField(max_length=6, choices=zone_type)

class classification_class(EmbeddedDocument):
	name = StringField(required=True)
	match_type = StringField(choices=match_type)
	matches = ListField(StringField())
	dscp_value = StringField()
	priorty = StringField()
	drop_prob = StringField()
class policing(EmbeddedDocument):
	cir = IntField(required=True)
	pir = IntField(required=True)
	dscp_transmit = StringField(required=True)
class shaping(EmbeddedDocument):
	peak = IntField(required=True)
	average = IntField(required=True)
class avoidance(EmbeddedDocument):
	drop_min_low = IntField()
	drop_min_med = IntField()
	drop_min_high = IntField()
	drop_max_low = IntField()
	drop_max_med = IntField()
	drop_max_high = IntField()
	denominator_low = IntField()
	denominator_med = IntField()
	denominator_high = IntField()
	ecn = BooleanField()
class regroupment_class(EmbeddedDocument):
	name = StringField(required=True)
	classes = classes = ListField(EmbeddedDocumentField(classification_class))
	shaping = EmbeddedDocumentField(shaping)
	policing = EmbeddedDocumentField(policing)
	avoidance = EmbeddedDocumentField(avoidance)

class policyIn(EmbeddedDocument):
	name = StringField(required=True)
	classes = ListField(EmbeddedDocumentField(classification_class))
class policyOut(EmbeddedDocument):
	name = StringField(required=True)
	classes = ListField(EmbeddedDocumentField(classification_class))
	regroupment_classes = ListField(EmbeddedDocumentField(regroupment_class))
class switch(switch):
	zone_type = StringField(max_length=6, choices=zone_type)
	policyIn = EmbeddedDocumentField(policyIn)
	policyOut = EmbeddedDocumentField(policyOut)
	def baseline(self):
		env = Environment(loader = FileSystemLoader(NET_CONF_TEMPLATES))
		template = env.get_template("baseline.j2")
		output = template.render(self = self)
class deparetment(EmbeddedDocument):
	name = StringField(max_length=6)
	address = StringField(max_length=6)
	priorty = StringField(max_length=6, choices=priorty)
class backup(EmbeddedDocument):
	starttime = StringField(max_length=6)
	endtime = StringField(max_length=6)
