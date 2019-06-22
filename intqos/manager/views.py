from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from jinja2 import Environment, FileSystemLoader
from intqos.settings import NET_CONF_TEMPLATES
import json
# Create your views here.
def index(request):
    # with open("/home/djoudi/IntelligentQoS/intqos/manager/application.json",'r') as jsonfile:
    #     ap=json.load(jsonfile)
    #     for app in ap['applications']:
    #         application(name=app['name'],match=app['match'],applicationType=app['applicationType']).save()
    #
    # apps=application.objects(applicationType="application-group")
    # policy = policyIn(name="policy",classes=apps)
    # camera = application.objects(name="ip-camera")
    # camera[0].priorty="4"
    # camera[0].drop_prob = "1"
    # camera[0].save()
    # app1 = application(name = "app1",match="match",priority = "1",drop_prob = "1")
    # app1.save()
    # app2 = application(name = "app12",match="match",priority = "1",drop_prob = "2")
    # app2.save()
    # app3 = application(name = "app13",match="match",priority = "1",drop_prob = "3")
    # app3.save()
    # app4 = application(name = "app14",match="match",priority = "2",drop_prob = "1")
    # app4.save()
    # app5 = application(name = "app15",match="match",priority = "2",drop_prob = "2")
    # app5.save()
    # app12 = application(name = "app112",match="match",priority = "2",drop_prob = "3")
    # app12.save()
    # app6 = application(name = "app16",match="match",priority = "3",drop_prob = "1")
    # app6.save()
    # app7 = application(name = "app17",match="match",priority = "3",drop_prob = "2")
    # app7.save()
    # app8 = application(name = "app18",match="match",priority = "3",drop_prob = "3")
    # app8.save()
    # app9 = application(name = "app19",match="match",priority = "4",drop_prob = "1")
    # app9.save()
    # app10 = application(name = "app110",match="match",priority = "4",drop_prob = "2")
    # app10.save()
    # app11 = application(name = "app111",match="match",priority = "4",drop_prob = "3")
    # app11.save()
    # classes = [app1,app2,app3,app4,app5,app6,app7,app8,app9,app10,app11]
    # int1=interface(interface_type="giga",interface_slot="0",interface_port="0",zone_type="Ingress")
    # int1.save()
    # int2=interface(interface_type="giga",interface_slot="1",interface_port="1",zone_type="Egress")
    # int2.save()
    # int3=interface(interface_type="giga",interface_slot="1",interface_port="3",zone_type="Egress")
    # int3.save()
    # int4=interface(interface_type="giga",interface_slot="1",interface_port="4",zone_type="Egress")
    # int4.save()
    # policy = policyIn(name="policcy",classes=classes)
    # policy.save()
    # swit = switch(hostname="router1",interfaces=[int2,int3,int4],zone_type="Ingress",policyIn=policy)
    #
    # swit.save()

    switches = switch.objects(hostname="router1")
    swit = switches[0]
    # print(swit.hostname)
    # for interface in swit.interfaces:
    #     if interface.zone_type=="Egress":
    #         print(interface.interface_name)
    #         highpolicing = policing(cir=10,pir=20,dscp_transmit="af11")
    #         high = regroupment_class(name="high",bandwidth="40",policing=highpolicing,classes=[app9,app10,app11],interface = interface)
    #         highpolicing.save()
    #         high.save()
    #         dscp(priority=4,drop_prob=3,drop_min=10,drop_max=15,denominator=5,regroupment_class=high).save()
    #         dscp(priority=4,drop_prob=2,drop_min=10,drop_max=15,denominator=5,regroupment_class=high).save()
    #         dscp(priority=4,drop_prob=1,drop_min=10,drop_max=15,denominator=5,regroupment_class=high).save()
    #         pripolicing = policing(cir=5,pir=10,dscp_transmit="af11")
    #         pri = regroupment_class(name="priorty",bandwidth="30",policing=pripolicing,classes=[app7,app8,app6],interface = interface)
    #         pripolicing.save()
    #         pri.save()
    #         dscp(priority=3,drop_prob=3,drop_min=10,drop_max=15,denominator=5,regroupment_class=pri).save()
    #         dscp(priority=3,drop_prob=2,drop_min=10,drop_max=15,denominator=5,regroupment_class=pri).save()
    #         dscp(priority=3,drop_prob=1,drop_min=10,drop_max=15,denominator=5,regroupment_class=pri).save()
    #         medpolicing = policing(cir=12,pir=12,dscp_transmit="af11")
    #         med = regroupment_class(name="med",bandwidth="20",policing=medpolicing,classes=[app4,app5,app12],interface = interface)
    #         medpolicing.save()
    #         med.save()
    #         dscp(priority=2,drop_prob=3,drop_min=10,drop_max=15,denominator=5,regroupment_class=med).save()
    #         dscp(priority=2,drop_prob=2,drop_min=10,drop_max=15,denominator=5,regroupment_class=med).save()
    #         dscp(priority=2,drop_prob=1,drop_min=10,drop_max=15,denominator=5,regroupment_class=med).save()
    #         lowpolicing = policing(cir=12,pir=12,dscp_transmit="af11")
    #         low = regroupment_class(name="low",bandwidth="10",policing=lowpolicing,classes=[app1,app2,app3],interface = interface)
    #         lowpolicing.save()
    #         low.save()
    #         dscp(priority=1,drop_prob=3,drop_min=10,drop_max=15,denominator=5,regroupment_class=low).save()
    #         dscp(priority=1,drop_prob=2,drop_min=10,drop_max=15,denominator=5,regroupment_class=low).save()
    #         dscp(priority=1,drop_prob=1,drop_min=10,drop_max=15,denominator=5,regroupment_class=low).save()
    #         p = policyOut(name="policyk"+str(interface.interface_name),interface = interface,regroupment_classes=[high,pri,med,low])
    #         p.save()





    # for interface in swit.interfaces:
    #     if interface.zone_type=="Egress":
    #         p=policyOut.objects(interface=interface)
    #         print(p[0].regroupment_classes[0].name)

    # print(classes[1])


    # for interface in swit.interfaces:
    #     if interface.zone_type=="Egress":
    #         a=regroupment_class(name="high",classes=[app9,app10,app11])
    #         a.save()
    #         b=regroupment_class(name="priorty",classes=[app8,app7,app6])
    #         b.save()
    #         c=regroupment_class(name="med",classes=[app12,app5,app4])
    #         c.save()
    #         d=regroupment_class(name="low",classes=[app1,app2,app3])
    #         d.save()
    #         p= policyOut(name="policyOut",regroupment_classes=[a,b,c,d])
    #         p.save()


    #print (camera.show_dscp)



    # policy.save()

    # topo=topology(topology_name="ahmed")
    # swit =switch(hostname="Router1")
    # topo.switches = [swit]
    # swit.zone_type="Ingress"
    # int1=interface(interface_type="giga",interface_slot="0",interface_port="0",zone_type="Ingress")
    # int2=interface(interface_type="giga",interface_slot="1",interface_port="1",zone_type="Egress")
    # # int3=interface(interface_type="giga",interface_slot="1",interface_port="3",zone_type="Egress")
    # # int4=interface(interface_type="giga",interface_slot="1",interface_port="4",zone_type="Egress")
    # swit.interfaces=[int1,int2]
    # int1.save()
    # int2.save()
    # # int3.save()
    # # int4.save()
    # topo.save()
    # server = deparetment(name="server",address="192.168.2.1",mask="255.255.255.0")
    # # costumers = deparetment(name="costumers",address="192.168.3.0",mask="255.255.255.0")
    # # print(server.wild_card)
    # time1=time_range(name="djoudi",begin="12:00",end='15:00')
    # filter1 = filter(name ='filter1',dest=server,time_range=time1)
    #
    # # filter2 = filter(name ='filter2',source=costumers)
    # ef = dscp(dscp_value="ef")
    # af41 = dscp(dscp_value="af41")
    # af42 = dscp(dscp_value="af42")
    # af43 = dscp(dscp_value="af43")
    # af32 = dscp(dscp_value="af32")
    # voice = application(name="voice",match_type="match-any",match='packet length min 64 max 200',dscp_value=ef)
    # database = application(name="database",match_type="match-any",match='protocol attribute category database',dscp_value=af41)
    # mail = application(name="mail",match_type="match-any",match='protocol attribute category email',dscp_value=af42)
    # backup = application(name="backup",match_type="match-any",match='protocol attribute category backup-and-storage',dscp_value=af43)
    # video_surveillance = application(name="video-surveillance",match_type="match-any",match='application attribute sub-category video-surveillance',dscp_value=af43)
    # file_transfer = application(name="file-transfer",match_type="match-any",match='protocol attribute sub-category file-transfer',dscp_value=af32)
    # mailClass = classification_class(name ="mailclass",application=mail,match_type="match-all")
    # databaseClass = classification_class(name ="databaseClass",application=database,match_type="match-all")
    # backupClass = classification_class(name ="backupClass",filter=filter1,application=backup,match_type="match-all")
    # videoClass = classification_class(name ="videoClass",application=video_surveillance,match_type="match-all")
    # fileClass = classification_class(name ="fileClass",application=file_transfer,match_type="match-all")
    # voiceClass = classification_class(name ="voiceClass",application=voice,match_type="match-all")
    # # mail2 = classification_class(name ="class2",application=app2,match_type="match-all")
    # labIn=policyIn(name="labIn",classes=[voiceClass,fileClass,videoClass,backupClass,databaseClass,mailClass])
    # swit.policyIn=labIn
    # voice.save()
    # database.save()
    # mail.save()
    # # server.save()
    # # filter1.save()
    # # time1.save()
    # backup.save()
    # video_surveillance.save()
    # file_transfer.save()
    # mailClass.save()
    # databaseClass.save()
    # backupClass.save()
    # videoClass.save()
    # fileClass.save()
    # voiceClass.save()
    # labIn.save()
    #
    # ef.save()
    # af41.save()
    # af42.save()
    # af43.save()
    # af32.save()
    #
    # voiceOut = regroupment_class(name="voiceOut",classes = [voice])
    # management = regroupment_class(name="management",classes = [database,backup,mail,video_surveillance])
    # LabOut=policyOut(name="LabOut",regroupment_classes=[voiceOut,management])
    #
    #
    # swit.policyOut=LabOut
    # voiceOut.save()
    # management.save()
    # LabOut.save()
    # swit.save()
    env = Environment(loader=FileSystemLoader(NET_CONF_TEMPLATES))
    baseline = env.get_template("base.j2")
    policies = policy_out.objects
    dscp_list = dscp.objects
    print(dscp_list)
    output = baseline.render(switch=swit, policies=policies, dscp_list=dscp_list)
    print(output)
    # # Nobaseline = env.get_template("Nobaseline.j2")
    # NoPolicyOut = env.get_template("NoPolicyOut.j2")
    # acl = env.get_template("acl.j2")
    # output = baseline.render(policyIn = policy)
    #print(output)
    # output3 = Nobaseline.render(swit = swit)
    # output4 = NoPolicyOut.render(swit = swit)
    # output2 = acl.render(classe = backupClass)
    # from netmiko import ConnectHandler
    # device_info = {"device_type" : "cisco_ios","ip" : "192.168.1.1","username" : "djoudi","password" : "djoudi","secret": "djoudi"}
    # device = ConnectHandler(**device_info)
    # config_commands = output4.splitlines()
    # config_commands2 = output4.splitlines()
    # device.enable()
    # device.send_config_set(config_commands)
    # # device.send_config_set(config_commands2)
    # print(output3)
    # print(output4)
    return HttpResponse("camera.show_dscp")
