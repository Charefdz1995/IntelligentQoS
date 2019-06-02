from .models import * 


def packet_parser(self):
	flow_instance = flow()
	flow_instance.ipv4_src_addr = self[NetflowRecordV9].IPV4_SRC_ADDR
	flow_instance.ipv4_dst_addr = self[]
	flow_instance.ipv4_protocol = self[]
	flow_instance.transport_src_port = self[]
	flow_instance.transport_dst_port = self[]
	flow_instance.type_of_service = self[]
	flow_instance.application_name = self[]
	flow_instance.counter_bytes = self[]
	flow_instance.counter_pkts = self[]
	flow_instance.first_switched = self[]
	flow_instance.last_switched = self[]
	flow_instance.collection_time = self[]
	flow_instance.interface_index = self[]
	flow_instance.device = self[] # TODO : some work here quering the db searching for who send this packets
	flow_instance.save()

