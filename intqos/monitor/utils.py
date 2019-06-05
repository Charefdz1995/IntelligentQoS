from .models import * 
import hashlib 

def packet_parser(self):
	# get the collection time before saving the flows to database. 
	sys_uptime = self[NetflowHeaderV9].sysUptime
	device = monitor.objects(loopback_addr = self[IP].src) 
	for record in self[NetflowDataflowsetV9].records:
		flow_input = record.IPV4_SRC_ADDR + ":" + record.L4_SRC_PORT +
					 "->"+ +record.IPV4_DST_ADDR + ":" + record.L4_SRC_PORT + 
					 "|"+ str(record.TOS) + "|" + str(int.from_bytes(record.APPLICATION_ID,'big'))
		flow_hash = hashlib.md5(flow_input.encode())

		netflow_fields_instance = netflow_fields()
		netflow_instance.counter_bytes = int.from_bytes(record.IN_BYTES,'big')
		netflow_instance.counter_pkts = int.from_bytes(record.IN_PKTS,'big')
		netflow_instance.first_switched = record.FIRST_SWITCHED
		netflow_instance.last_switched = record.LAST_SWITCHED
		netflow_instance.bandwidth = (record.LAST_SWITCHED - record.FIRST_SWITCHED) / 1000 * 8 * record.IN_PKTS # bandwidth in bps 
		netflow_instance.interface_index = int.from_bytes(record.INPUT_SNMP,'big')
		netflow_instance.collection_time = sys_uptime # the collection time isdefined before in this function
		netflow_instance.device = device # TODO : some work here quering the db searching for who send this packets


		flow = monitor.objects(id= flow_hash.hexdigest())

		if flow = None: 
			flow_instance = flow()
			flow_instance.ipv4_src_addr = record.IPV4_SRC_ADDR
			flow_instance.ipv4_dst_addr = record.IPV4_DST_ADDR
			flow_instance.ipv4_protocol = record.PROTOCOL 
			flow_instance.transport_src_port = record.L4_SRC_PORT
			flow_instance.transport_dst_port = record.L4_DST_PORT
			flow_instance.type_of_service = record.TOS # check for network byte order in this RFC
			flow_instance.application_name = int.from_bytes(record.APPLICATION_ID,'big')
			flow_instance.save()
			netflow_instance.flow = flow_instance
			netflow_instance.save()
		else :			
			netflow_instance.flow = flow 
			netflow_instance.save()


