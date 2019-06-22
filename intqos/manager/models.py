from django.db import models

# Create your models here.
from mongoengine import *
from common.models import *

zone_type = (('Egress', 'Egress'), ('Ingress', 'Ingress'))
match_type = ('match-any', 'match-all')
priority = (('high', '4'), ('priorty', '3'), ('medium', '2'), ('low', '1'))
drop_prob = (('high', '3'), ('medium', '2'), ('low', '1'))
app_type = (
'Application', 'Protocol', 'application-group', 'device-class', 'media-type', 'Attribute', 'Category', 'sub-category')


# class deparetment(EmbeddedDocument):
# 	name = StringField()
# 	address = StringField()
# 	mask = StringField()
# 	@property
# 	def wild_card(self):
# 		wildcard = []
# 		for x in self.mask.split('.'):
#         		a=255-int(x)
#         		wildcard.append(a)
# 		a=''
# 		for x in wildcard:
#         		a=a+str(x)
#         		if wildcard.index(x)<3:
#                 		a=a+'.'
# 		return a
# class time_range(EmbeddedDocument):
# 	name=StringField()
# 	begin=StringField()
# 	end=StringField()
#
# class filter(EmbeddedDocument):
# 	name = StringField()
# 	source = EmbeddedDocumentField(deparetment)
# 	dest = EmbeddedDocumentField(deparetment)
# 	time_range=EmbeddedDocumentField(time_range)
# 	acl = StringField()
# class dscp(EmbeddedDocument):
# 	dscp_value=StringField(required=True)
# 	jitter_ref= StringField()
# 	delay_ref= StringField()
# 	packetloss_ref= StringField()
# 	bandwith_ref= StringField()
#
# class application(EmbeddedDocument):
# 	name = StringField(required=True)
# 	match = StringField()
# 	dscp_value = EmbeddedDocumentField(dscp)
# 	priorty = StringField()
# 	drop_prob = StringField()
# 	match_type = StringField(choices=match_type)
# class classification_class(EmbeddedDocument):
# 	name = StringField()
# 	application = EmbeddedDocumentField(application)
# 	filter = EmbeddedDocumentField(filter)
# 	match_type = StringField(choices=match_type)
# #------------------------------------------------------------------------
#
# class interface(interface_base):
# 	zone_type = StringField(choices=zone_type)
# class policing(EmbeddedDocument):
# 	cir = IntField(required=True)
# 	pir = IntField(required=True)
# 	dscp_transmit = StringField(required=True)
# class shaping(EmbeddedDocument):
# 	peak = IntField(required=True)
# 	average = IntField(required=True)
# class avoidance(EmbeddedDocument):
# 	drop_min_low = IntField()
# 	drop_min_med = IntField()
# 	drop_min_high = IntField()
# 	drop_max_low = IntField()
# 	drop_max_med = IntField()
# 	drop_max_high = IntField()
# 	denominator_low = IntField()
# 	denominator_med = IntField()
# 	denominator_high = IntField()
# 	ecn = BooleanField()
# class regroupment_class(EmbeddedDocument):
# 	name = StringField(required=True)
# 	classes = ListField(EmbeddedDocumentField(application))
# 	shaping = EmbeddedDocumentField(shaping)
# 	policing = EmbeddedDocumentField(policing)
# 	avoidance = EmbeddedDocumentField(avoidance)
#
# class policyIn(EmbeddedDocument):
# 	name = StringField(required=True)
# 	classes = ListField(EmbeddedDocumentField(classification_class))
# class policyOut(EmbeddedDocument):
# 	name = StringField(required=True)
# 	classes = ListField(EmbeddedDocumentField(classification_class))
# 	regroupment_classes = ListField(EmbeddedDocumentField(regroupment_class))
# class switch(switch):
# 	zone_type = StringField(choices=zone_type)
# 	policyIn = EmbeddedDocumentField(policyIn)
# 	policyOut = EmbeddedDocumentField(policyOut)
# 	def baseline(self):
# 		env = Environment(loader = FileSystemLoader(NET_CONF_TEMPLATES))
# 		template = env.get_template("baseline.j2")
# 		output = template.render(self = self)
# 		return output


class application(Document):
    name = StringField()
    num = StringField()
    policy = BooleanField(default=False)
    application_type = StringField(choices=app_type)
    match = StringField()
    priority = StringField(required=False)
    drop_prob = StringField(required=False)
    bandwidth = StringField()

    @property
    def dscp_value(self):
        return "AF{}{}".format(self.priority, self.drop_prob)


# class custom(EmbeddedDocument):
# 	name = StringField()
# 	match = StringField()
# 	priority = StringField(choices=priority)
# 	drop_prob = StringField(choices=drop_prob)
# 	dscp_value = 'AF'+priority+drop_prob


class policing(EmbeddedDocument):
    cir = IntField(required=True)
    pir = IntField(required=True)
    dscp_transmit = StringField()


# class shaping(EmbeddedDocument):
# 	peak = IntField(required=True)
# 	average = IntField(required=True)
# class avoidance(EmbeddedDocument):

# 	drop_max_low = IntField()
# 	drop_max_med = IntField()
# 	drop_max_high = IntField()
# 	denominator_low = IntField()
# 	denominator_med = IntField()
# 	denominator_high = IntField()
# 	ecn = BooleanField()

class interface(interface):
    zone_type = StringField(choices=zone_type)


class policy_in(Document):
    name = StringField(required=True)
    classes = ListField(ReferenceField(application))


class regroupment_class(Document):
    name = StringField(required=True)
    classes = ListField(ReferenceField(application))
    bandwidth = StringField()
    interface = ReferenceField(interface)
    policing = EmbeddedDocumentField(policing)


class policy_out(Document):
    name = StringField(required=True)
    interface = ReferenceField(interface)
    regroupment_classes = ListField(ReferenceField(regroupment_class))


class switch(device):
    zone_type = StringField(choices=zone_type)
    policy_in = ReferenceField(policy_in)


class dscp(Document):
    regroupment_class = ReferenceField(regroupment_class)
    applications = ListField(ReferenceField(application))
    priority = IntField(required=False)
    drop_prob = IntField(required=False)
    jitter_ref = StringField()
    delay_ref = StringField()
    packetloss_ref = StringField()
    bandwith_ref = StringField()
    drop_min = IntField()
    drop_max = IntField()
    denominator = IntField()

    @property
    def dscp_value(self):
        return "AF{}{}".format(self.priority, self.drop_prob)
