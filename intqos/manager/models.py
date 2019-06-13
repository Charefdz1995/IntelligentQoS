from django.db import models

# Create your models here.
from mongoengine import *
from common.models import *
from jinja2 import Environment, FileSystemLoader
from intqos.settings import NET_CONF_TEMPLATES

zone_type = (('Egress', 'Egress'),('Ingress', 'Ingress'))
match_type =('match-any','match-all')
priorty =('high','priority','normal','low')

class deparetment(EmbeddedDocument):
	name = StringField()
	address = StringField()
	mask = StringField()
	@property
	def wild_card(self):
		wildcard = []
		for x in self.mask.split('.'):
        		a=255-int(x)
        		wildcard.append(a)
		a=''
		for x in wildcard:
        		a=a+str(x)
        		if wildcard.index(x)<3:
                		a=a+'.'
		return a

class filter(EmbeddedDocument):
	name = StringField()
	source = EmbeddedDocumentField(deparetment)
	dest = EmbeddedDocumentField(deparetment)
	acl = StringField()
class dscp(EmbeddedDocument):
	dscp_value=StringField(required=True)
	jitter_ref= StringField()
	delay_ref= StringField()
	packetloss_ref= StringField()
	bandwith_ref= StringField()

class application(EmbeddedDocument):
	name = StringField(required=True)
	match = StringField()
	dscp_value = EmbeddedDocumentField(dscp)
	priorty = StringField()
	drop_prob = StringField()
	match_type = StringField(choices=match_type)
class classification_class(EmbeddedDocument):
	name = StringField()
	application = EmbeddedDocumentField(application)
	filter = EmbeddedDocumentField(filter)
	match_type = StringField(choices=match_type)
#------------------------------------------------------------------------

class interface(interface_base):
	zone_type = StringField(choices=zone_type)
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
	classes = ListField(EmbeddedDocumentField(application))
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
	zone_type = StringField(choices=zone_type)
	policyIn = EmbeddedDocumentField(policyIn)
	policyOut = EmbeddedDocumentField(policyOut)
	def baseline(self):
		env = Environment(loader = FileSystemLoader(NET_CONF_TEMPLATES))
		template = env.get_template("baseline.j2")
		output = template.render(self = self)
		return output
