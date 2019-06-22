from django.contrib.auth.decorators import login_required
from mongoengine import *
from django.shortcuts import render, redirect
from common.models import *
# Create your views here.

from gui.forms import *

from common.models import topology


@login_required(login_url='/login/')
def home(request):
    ctx = {}
    return render(request,'home.html',context=ctx)


def drag_drop(request,topo_id):
    # tp = topology.objects(id=topo_id)
    # if (topology.fileLoc == None):
    #     JsonFile = GetJsonFile(initial={'Text': """{ "class": "go.GraphLinksModel",
    #           "copiesArrays": true,
    #           "copiesArrayObjects": true,
    #           "linkFromPortIdProperty": "fromPort",
    #           "linkToPortIdProperty": "toPort",
    #           "nodeDataArray": [],
    #           "linkDataArray": []}"""})
    # else:
    #     with open(topology.fileLoc, 'r') as file:
    #         data = file.read().replace('\n', '')
    #
    #     JsonFile = GetJsonFile(initial={'Text': data})
    #
    # ctx = {'json': JsonFile, 'id': topo_id}
    ctx={}
    return render(request, 'dragndrop.html', context=ctx)



def add_topology(request):
    TopoForm = AddTopologyForm(request.POST)
    if TopoForm.is_valid():
        tp = topology(topology_name=request.POST['Name'], topology_desc=request.POST['TopologyDesc'])
        tp.save()
    return redirect('Home')

def topologies(request):
    TopoForm = AddTopologyForm()
    topologies = topology.objects
    ctx = {'topology':TopoForm,'topologies':topologies}
    return render(request,'draw.html',context = ctx)

def DrawTopology(request,topo_id):

    JsonFile = GetJsonFile(initial={'Text': """{ "class": "go.GraphLinksModel",
            "copiesArrays": true,
            "copiesArrayObjects": true,
            "linkFromPortIdProperty": "fromPort",
            "linkToPortIdProperty": "toPort",
            "nodeDataArray": [],
            "linkDataArray": []}"""})
    ctx = {'json':JsonFile,'id':topo_id}
    return render(request,'dragndrop.html',context=ctx)
