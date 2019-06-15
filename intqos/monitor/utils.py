from .models import * 
import hashlib 

def dbcollect(pkt):
        mongoengine.connect("flows", host = "192.168.10.10",port = 27017)
        sys_uptime = pkt[NetflowHeaderV9].sysUptime
        monitor = monitor.objects(loopback_addr = pkt[IP].src)
        flows = None
        try:
                flows = pkt[NetflowDataflowsetV9].records
        except Exception as e :
                print(e)
        try:
						# fill the fields of netflow in each monitor
						netflow_fields_ins = netflow_fields()
						netflow_fields_ins.counter_bytes = int.from_bytes(record.IN_BYTES,'big')
						netflow_fields_ins.counter_pkts = int.from_bytes(record.IN_PKTS,'big')
						netflow_fields_ins.first_switched = record.FIRST_SWITCHED
						netflow_fields_ins.last_switched = record.LAST_SWITCHED
						netflow_fields_ins.input_int = int.from_bytes(record.INPUT_SNMP,'big')
						netflow_fields_ins.output_int = int.from_bytes(record.OUTPUT_SNMP,'big')
						netflow_fields_ins.collection_time = sys_uptime

						#calculate the bandwidth in bps
						netflow_fields_ins.bandwidth = (record.LAST_SWITCHED - record.FIRST_SWITCHED) / 1000 * 8 * record.IN_PKTS  


						# create the flow and verify if it exist
						flow_input = record.IPV4_SRC_ADDR + ":" + record.L4_SRC_PORT +"->"+ +record.IPV4_DST_ADDR + ":" + record.L4_SRC_PORT + "|"+ str(record.TOS) + "|" + str(int.from_bytes(record.APPLICATION_ID,'big'))
						flow_hash = hashlib.md5(flow_input.encode())
						flow_exist = monitor.objects(id= flow_hash.hexdigest())
						if not(flow_exist) : 
                        	flow_ins = flow()
                        	flow_ins.ipv4_src_addr = record.IPV4_SRC_ADDR
                        	flow_ins.ipv4_dst_addr = record.IPV4_DST_ADDR
                        	flow_ins.ipv4_protocol = record.PROTOCOL
                        	flow_ins.transport_src_port = record.L4_SRC_PORT
                        	flow_ins.transport_dst_port = record.L4_DST_PORT
                        	flow_ins.type_of_service = record.TOS
                        	flow_ins.application_name = int.from_bytes(record.APPLICATION_ID,'big')
                        	flow_ins.save()
                        	netflow_fields_ins.flow = flow_ins
							netflow_fields_ins.device = monitor
                        	netflow_fields_ins.save()
                        else:
                        	netflow_fields_ins.device = monitor
                        	netflow_fields_ins.flow = flow_exist
                        	netflow_fields_ins.save()



        except Exception as e :
                print(e)