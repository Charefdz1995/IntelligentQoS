from django.db import models

# Create your models here.
from mongoengine import * 
from common.models import * 
zone_type = (('Egress', 'Egress'),('Ingress', 'Ingress'))

class interface(interface_base):
	zone_type = StringField(max_length=6, choices=zone_type)
class switch(switch):
	zone_type = StringField(max_length=6, choices=zone_type)

