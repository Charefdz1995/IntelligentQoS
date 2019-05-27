from mongoengine import * 
from common.models import * 
from jinja2 import Environment, FileSystemLoader
from intqos.settings import NET_CONF_TEMPLATES
from exception import * 


class interface(interface_base):

	def configure_netflow(self):
		output = ""
		env = Environment(loader = FileSystemLoader(NET_CONF_TEMPLATES))
		template = env.get_template("netflow_interface_config")
		output = template.render(self = self)
		return output


class monitor(switch):
		
	def configure_netflow(self,**kwargs):
		global_output = ""
		interfaces_output = ""
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
				if kwarg not in expected_kwargs:
					raise NotDefinedParameter

		output = template.render(kwargs = kwargs,self= self)

		except NotExistingDestination as e:
			print(e)
		except NotDefinedParameter as e  :
			print(e)


		for interface in self.interfaces : 
			interfaces_output += interface.configure_netflow()

		return global_output + interfaces_output
	
	def push_configuration(self,config):

		from netmiko import ConnectHandler 

		device_info = {
			"device_type" : "cisco_ios", 
			"ip" : self.management.management_address,
			"username" : self.management.username, 
			"password" : self.management.password, 
		}

		try:
			device = ConnectHandler(**device_info)
			config_commands = config.splitlines()
			device.send_config_set(config_commands)
			device.disconnect()
		except Exception as e:
			print (e) 
		 
		


class phb_domain(topology):

	def configure_loopback(self):
		i = 1 
		for switch in self.switches:
			switch.loopback_addr = '{}.{}.{}.{}'.format(str(i),str(i),
														str(i),str(i))
			i += 1

	def configure_netflow(self,**kwargs):
		for switch in switches:
			switch.__class__ = monitor
			configuration = switch.configure_netflow(kwargs.items)
			switch.push_configuration(configuration)



class netflow_collector(Document):
	pass 