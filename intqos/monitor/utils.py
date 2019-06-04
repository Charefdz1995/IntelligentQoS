from .models import * 


def packet_parser(self):
	# get the collection time before saving the flows to database. 
	sys_uptime = self[NetflowHeaderV9].sysUptime
	device = monitor.objects(loopback_addr = self[IP].src) 
	for record in self[NetflowDataflowsetV9].records:
		flow_instance = flow()
		flow_instance.ipv4_src_addr = record.IPV4_SRC_ADDR
		flow_instance.ipv4_dst_addr = record.IPV4_DST_ADDR
		flow_instance.ipv4_protocol = record.PROTOCOL 
		flow_instance.transport_src_port = record.L4_SRC_PORT
		flow_instance.transport_dst_port = record.L4_DST_PORT
		flow_instance.type_of_service = record.TOS # check for network byte order in this RFC
		flow_instance.application_name = int.from_bytes(record.APPLICATION_ID,'big') 
		flow_instance.counter_bytes = int.from_bytes(record.IN_BYTES,'big')
		flow_instance.counter_pkts = int.from_bytes(record.IN_PKTS,'big')
		flow_instance.first_switched = record.FIRST_SWITCHED
		flow_instance.last_switched = record.LAST_SWITCHED
		flow_instance.bandwidth = (record.LAST_SWITCHED - record.FIRST_SWITCHED) / 1000 * 8 * record.IN_PKTS # bandwidth in bps 
		flow_instance.interface_index = int.from_bytes(record.INPUT_SNMP,'big')
		flow_instance.collection_time = sys_uptime # the collection time isdefined before in this function
		flow_instance.device = device # TODO : some work here quering the db searching for who send this packets
		flow_instance.save()

