from .models import * 
import hashlib 
from mongoengine import *
import mongoengine
from scapy.all import * 
from scapy.layers.netflow import NetflowSession
from jinja2 import Environment, FileSystemLoader
from intqos.settings import NET_CONF_TEMPLATES
import re 

def dbcollect(pkt,phb_behavior):
        mongoengine.connect("flowsdb", host = "0.0.0.0",port = 27017)
        sys_uptime = pkt[NetflowHeaderV9].sysUptime
        monitor  = device.objects(pkt[IP].src)[0]
        flows = None
        try:
                flows = pkt[NetflowDataflowsetV9].records
        except Exception as e :
                print(e)
        try:
                for record in flows:

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
                        #netflow_fields_ins.bandwidth = (record.LAST_SWITCHED - record.FIRST_SWITCHED) / 1000 * 8 * record.IN_PKTS  


                        # create the flow and verify if it exist
                        flow_input = "{}:{}->{}:{}|{}|{}|{}".format(str(record.IPV4_SRC_ADDR),str(record.L4_SRC_PORT),str(record.IPV4_DST_ADDR) , str(record.L4_SRC_PORT) ,str(record.TOS) , str(int.from_bytes(record.APPLICATION_ID,'big')),str(record.PROTOCOL))

                        flow_hash = hashlib.md5(flow_input.encode())
                        print("quering the database if flow exists")
                        flow_exist = None
                        flow_exist = flow.objects(flow_id= flow_hash.hexdigest())
                        if not(flow_exist) :
                                print("new flow is occured")
                                flow_ins = flow()
                                flow_ins.flow_id = str(flow_hash.hexdigest())
                                flow_ins.ipv4_src_addr = record.IPV4_SRC_ADDR
                                flow_ins.ipv4_dst_addr = record.IPV4_DST_ADDR
                                flow_ins.ipv4_protocol = record.PROTOCOL
                                flow_ins.transport_src_port = record.L4_SRC_PORT
                                flow_ins.transport_dst_port = record.L4_DST_PORT
                                flow_ins.type_of_service = record.TOS
                                flow_ins.application_name = int.from_bytes(record.APPLICATION_ID,'big')
                                flow_ins.save()
                                netflow_fields_ins.flow_ref = flow_ins
                                netflow_fields_ins.device = monitor
                                netflow_fields_ins.save()
                                print("new flow is added")
                                print("new ip sla is configured for this flow")
                        else:
                                netflow_fields_ins.device = monitor
                                netflow_fields_ins.flow_ref = flow_exist[0]
                                netflow_fields_ins.save()
                                print("an old flow informationare added is added")
                                print("pull ip sla information")           
        

        except Exception as e :
                print(e)


def Sniff_Netflow():
        sniff(session = NetflowSession , filter = "dst port 2055", prn = dbcollect)








def get_ip_sla_devices(src_ip, src_dst):
        pass 
