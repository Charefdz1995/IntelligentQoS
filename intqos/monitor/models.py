from mongoengine import * 
from common.models import * 
from jinja2 import Environment, FileSystemLoader
from intqos.settings import NET_CONF_TEMPLATES


class interface(interface):

	def configure_netflow(self):
		output = ""
		env = Environment(loader = FileSystemLoader(NET_CONF_TEMPLATES))
		template = env.get_template("netflow_interface_config")
		output = template.render(self = self)
		return output


class device(device):

	networks = ListField(StringField())
	def get_networks(self):
		for interface in self.
	def configure_netflow(self,destination):
		global_output = ""
		interfaces_output = ""

		env = Environment(loader=FileSystemLoader(NET_CONF_TEMPLATES))
		template = env.get_template("global_netflow_config.j2")
		
		output = template.render(dst = destination)

		for interface in self.interfaces : 
			interfaces_output += interface.configure_netflow()

		return global_output + interfaces_output

	def configure_ip_sla(self,operation,dst_ip,dst_port,src_ip,src_port):
        env = Environment(loader=FileSystemLoader(NET_CONF_TEMPLATES))
        template = env.get_template("ip_sla.j2")
                
        output = template.render(operation = operation,dst_ip =dst_ip,
                                dst_port = dst_port ,src_ip = src_ip ,src_port = src_port)

        return output

    def configure_ip_sla_responder(self):
    	return ["ip sla responder"]


	def push_config(self,config_commands)
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
			print(e)


class topology(topology):
	def get_ip_sla_devices(self,record):
		src_ip = record.IPV4.SRC.ADDR 
		dst_ip = record.IPV4.DST.ADDR 
		for device in self.devices:



class flow(DynamicDocument):
	ipv4_src_addr = StringField(required = True)
	ipv4_dst_addr = StringField(required = True)
	ipv4_protocol = IntField(required = True)
	transport_src_port = IntField(required = True)
	transport_dst_port = IntField(required = True)
	type_of_service = IntField(required = True)
	application_name = StringField(required = True)
	
	

class netflow_fields(DynamicDocument):

	#Real time information about flow in the monitor. 
	counter_bytes = IntField(required = True)
	counter_pkts = IntField(required = True)
	first_switched = FloatField(required = True)
	last_switched  = FloatField(required = True)
	#QoS parameters
	bandwidth = FloatField(required = False)
	#=======================================
	# Device related Information
	collection_time = StringField(required = True)
	input_int = IntField(required = True)
	output_int = IntField(required = True)
	device = ReferenceField(device)
	flow = ReferenceField(flow)
	#=======================================

class ip_sla(document):
	operation = IntField(required= True)



class ip_sla_info(document):
	avg_jitter = IntField(required = True)
	avg_delay = IntField(required = True)
    packet_loss = IntField(required = True)
    timestamp = StringField(required = True)
    flow_ref = ReferenceField(flow)
    ip_sla_info = ReferenceField(ip_sla)
