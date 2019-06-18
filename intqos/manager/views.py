# from django.shortcuts import render
# from django.http import HttpResponse
#
# from intqos.common.models import topology
# from .models import *
# from jinja2 import Environment, FileSystemLoader
# from intqos.intqos.settings import NET_CONF_TEMPLATES
#
# # Create your views here.
# def index(request):
#     topo=topology(topology_name="ahmed")
#     swit =switch(hostname="r1")
#     topo.switches = [swit]
#     swit.zone_type="Ingress"
#     int1=interface(interface_type="giga",interface_slot="1",interface_port="1",zone_type="Ingress")
#     int2=interface(interface_type="giga",interface_slot="1",interface_port="2",zone_type="Egress")
#     int3=interface(interface_type="giga",interface_slot="1",interface_port="3",zone_type="Egress")
#     int4=interface(interface_type="giga",interface_slot="1",interface_port="4",zone_type="Egress")
#     swit.interfaces=[int1,int2,int3,int4]
#     int1.save()
#     int2.save()
#     int3.save()
#     int4.save()
#     topo.save()
#     # server = deparetment(name="server",address="192.168.2.1",mask="255.255.255.0")
#     # costumers = deparetment(name="costumers",address="192.168.3.0",mask="255.255.255.0")
#     # print(server.wild_card)
#     # filter1 = filter(name ='filter1',dest=server)
#     # filter2 = filter(name ='filter2',source=costumers)
#     ef = dscp(dscp_value="ef")
#     af41 = dscp(dscp_value="af41")
#     af42 = dscp(dscp_value="af42")
#     af43 = dscp(dscp_value="af43")
#     af32 = dscp(dscp_value="af32")
#     voice = application(name="voice",match_type="match-any",match='packet length min 64 max 200',dscp_value=ef)
#     database = application(name="database",match_type="match-any",match='protocol attribute category database',dscp_value=af41)
#     mail = application(name="mail",match_type="match-any",match='protocol attribute category email',dscp_value=af42)
#     backup = application(name="backup",match_type="match-any",match='protocol attribute category backup-and-storage',dscp_value=af43)
#     video_surveillance = application(name="video-surveillance",match_type="match-any",match='application attribute sub-category video-surveillance',dscp_value=af43)
#     file_transfer = application(name="file-transfer",match_type="match-any",match='protocol attribute sub-category file-transfer',dscp_value=af32)
#     mailClass = classification_class(name ="mailclass",application=mail,match_type="match-all")
#     databaseClass = classification_class(name ="databaseClass",application=database,match_type="match-all")
#     backupClass = classification_class(name ="backupClass",application=backup,match_type="match-all")
#     videoClass = classification_class(name ="videoClass",application=video_surveillance,match_type="match-all")
#     fileClass = classification_class(name ="fileClass",application=file_transfer,match_type="match-all")
#     voiceClass = classification_class(name ="voiceClass",application=voice,match_type="match-all")
#     # mail2 = classification_class(name ="class2",application=app2,match_type="match-all")
#     labIn=policyIn(name="labIn",classes=[voiceClass,fileClass,videoClass,backupClass,databaseClass,mailClass])
#     swit.policyIn=labIn
#     voice.save()
#
#     database.save()
#     mail.save()
#     backup.save()
#     video_surveillance.save()
#     file_transfer.save()
#     mailClass.save()
#     databaseClass.save()
#     backupClass.save()
#     videoClass.save()
#     fileClass.save()
#     voiceClass.save()
#     labIn.save()
#
#     ef.save()
#     af41.save()
#     af42.save()
#     af43.save()
#     af32.save()
#
#     voiceOut = regroupment_class(name="voiceOut",classes = [voice])
#     management = regroupment_class(name="management",classes = [database,backup,mail,video_surveillance])
#     LabOut=policyOut(name="LabIn",regroupment_classes=[voiceOut,management])
#
#
#     swit.policyOut=LabOut
#     voiceOut.save()
#     management.save()
#     LabOut.save()
#     swit.save()
#     env = Environment(loader = FileSystemLoader(NET_CONF_TEMPLATES))
#     template = env.get_template("baselineconfig.j2")
#     output = template.render(swit = swit)
#     from netmiko import ConnectHandler
#     device_info = {
# 		"device_type" : "cisco_ios",
# 		"ip" : "192.168.1.1",
# 		"username" : "djoudi",
# 		"password" : "djoudi",
#         'secret': 'djoudi',
# 		}
#         # device = ConnectHandler(**device_info)
# 		# config_commands = output.splitlines()
# 		# device.send_config_set(config_commands)
# 		# device.disconnect()
#     print(output)
#     return HttpResponse('ahhhhh')
#
