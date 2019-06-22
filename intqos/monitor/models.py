import re
from netaddr import *
from mongoengine import *
from common.models import *
from jinja2 import Environment, FileSystemLoader
from napalm import get_network_driver 
from intqos.settings import NET_CONF_TEMPLATES
import numpy as np 
from .utils import valid_cover



class interface(interface):

	def configure_netflow(self):
		output = ""
		env = Environment(loader = FileSystemLoader(NET_CONF_TEMPLATES))
		template = env.get_template("netflow_interface_config")
		output = template.render(self = self)
		return output


class device(device):

	def configure_netflow(self,destination):
		global_output = ""
		interfaces_output = ""

		env = Environment(loader=FileSystemLoader(NET_CONF_TEMPLATES))
		template = env.get_template("global_netflow_config.j2")
		output = template.render(dst = destination)
		for interface in self.interfaces : 
			interfaces_output += interface.configure_netflow()

		config = (global_output + interfaces_output).splitlines()

		return self.connect().cli(config)

	def configure_ip_sla(self,operation,record):
		env = Environment(loader=FileSystemLoader(NET_CONF_TEMPLATES))
		template = env.get_template("ip_sla.j2")
		output = template.render(operation = operation,record = record)
		config = output.splitlines()
		return self.connect().cli(config)


	def configure_ip_sla_responder(self):
		return self.connect().cli(['ip sla responder'])


	def pull_ip_sla_stats(self,operation,src_device):
		jitter_cmd = "show ip sla statistics {} | include Destination to Source Jitter".format(str(operation))
		delay_cmd = "show ip sla statistics {} | include Destination to Source Latency".format(str(operation))
		config = [jitter_cmd,delay_cmd]

		result = self.connect().cli(config)

		jitter = int(re.findall("\+d",result[jitter_cmd])[1])
		delay = int(re.findall("\+d",result[delay_cmd])[1])

		return jitter, delay

	def connect(self):
		driver = get_network_driver("ios")
		device = None
		try:
			device = driver(self.management.management_address,self.management.username,
							self.management.password)
			device.open()
		except Exception as e:
			print(e)
		return device


class topology(topology):

	def get_ip_sla_devices(self,record):
		src_ip = IPAddress(record.IPV4.SRC.ADDR) 
		dst_ip = IPAddress(record.IPV4.DST.ADDR)
		src_device = None
		dst_device = None  
		for device in self.devices:
			for interface in device.interfaces:
				net_mask = IPAddress(interface.interface_mask)
				network = IPNetwork(interface.interface_address)
				network.prefixlen = net_mask.netmask_bits()
				if src_ip in network:
					src_device = device
				if dst_ip in network:
					dst_device = device
		return src_device,dst_device

	def vertex(self):
		devices_num = len(self.devices)
		matrix = np.zeros(shape = (devices_num,devices_num))
		for link in self.links:
			row_index = self.devices.index(to_device)
			column_index = self.devices.index(from_device)
			matrix[row_index][column_index] = 1
			cover = []

		valid, num_edge = valid_cover(matrix, cover)
		while not valid:
			m = [x for x in range(0, len(num_edge)) if num_edge[x] == max(num_edge)][0]
			cover.append(m)
			valid, num_edge = valid_cover(matrix, cover)

		monitors = []	
		for i in cover:
			monitors.append(self.devices[i])

		return monitors







	def kill_ip_sla(self): #TODO : killing the ip sla of inactive flows after 5 min 
		pass 







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

class ip_sla(Document):
	operation = SequenceField()
	device_ref = ReferenceField(device)




class ip_sla_info(Document):
	avg_jitter = IntField(required = True)
	avg_delay = IntField(required = True)
	packet_loss = IntField(required = False) # For the moment it is false because i dont know how to get it 
	timestamp = StringField(required = False) # temporary false until see how the netflow is sniffing the timestamp to combine it with ip sla 
	flow_ref = ReferenceField(flow)
	ip_sla_ref = ReferenceField(ip_sla)