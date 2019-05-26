from mongoengine import * 
from common.models import * 
from jinja2 import Environment, FileSystemLoader
from intqos.settings import NET_CONF_TEMPLATES
from exception import * 

class monitor(switch):
	loopback_address = StringField(required=True)
		
	def configure_netflow(self,**kwargs):
		output = ""
		expected_kwargs = ['destination','port','source','template_data_timeout',
							'application_table_timeout','application_attribute_timeout', 
							'cache_timeout_active','cache_timeout_inactive']
		env = Environment(loader=FileSystemLoader(NET_CONF_TEMPLATES))
		template = env.get_template("global_netflow_config.j2")
		try:

			destination = kwargs.get('destination')
			if destination == None:
				raise NotExistingDestination
			for kwarg in kwargs.items():
				if kwargs not in expected_kwargs:
					raise NotDefinedParameter

		output = template.render(kwargs = kwargs,self= self)

		except NotExistingDestination as e:
			print(e)
		except NotDefinedParameter as e  :
			print(e)
		

class phb_domain(topology):

	def configure_netflow(self):
		pass 

class netflow_collector(Document):
	pass 