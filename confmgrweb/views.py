from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from confmgrweb.settings import *
from confmgrweb.graph import *
import json

from django.shortcuts import redirect
from django.forms.models import model_to_dict


# Create your views here.
def index(request):
    return render(request, 'index.html')
def head(request):
    return render(request, 'head.html')
def left(request):
    return render(request, 'left.html')
def main(request):
    return render(request, 'main.html')
def tab(request):
    return  render(request,'tab.html',{'firewalllist':firewalllist})
def policytab(request):
    dev = request.GET.get('dev')
    policytype = request.GET.get('policytype')
    if not dev and not policytype:
        return  render(request,'policytab.html',{'firewalllist':firewalllist})
    else:
        for i in firewalllist:
            if i.name == dev:
                if policytype == 'policylist':
                    policydiclist = []
                    for j in i.policylist:
                        policydic={"id":j.name,"srceth":j.srceth,"dsteth":j.dsteth,"srcaddr":j.srcaddr,"dstaddr":j.dstaddr,"service":j.service}
                        policydiclist.append(policydic)
                    return JsonResponse({'policydic':policydiclist})
                elif policytype == 'policydetaillist':
                    policydiclist = []
                    for j in i.policydetaillist:
                        policydic = {"id": j.name, "srceth": j.srceth, "dsteth": j.dsteth, "srcaddr": j.srcaddr,
                                     "dstaddr": j.dstaddr, "service": j.service}
                        policydiclist.append(policydic)
                    return JsonResponse( {'policydic':policydiclist})
                elif policytype == 'policymiclist':
                    policydiclist = []
                    for j in i.policymiclist:
                        policydic = {"id": j.name, "srceth": j.srceth, "dsteth": j.dsteth, "srcaddr": j.srcaddr,
                                     "dstaddr": j.dstaddr, "service": j.service}
                        policydiclist.append(policydic)
                    return JsonResponse({'policydic': policydiclist})
def repolicytab(request):
    dev =request.GET.get("dev")
    if not dev :
        return render(request, 'repolicytab.html', {'firewalllist': firewalllist})
    else:
        for i in firewalllist:
            if i.name == dev:
                redundantpolicylist =i.redundantcheck()
        policydiclist = []
        for j in redundantpolicylist:
            policydic = {"id": j.name, "srceth": j.srceth, "dsteth": j.dsteth, "srcaddr": j.srcaddr,
                         "dstaddr": j.dstaddr, "service": j.service}
            policydiclist.append(policydic)
        return JsonResponse({'repolicytab': policydiclist})
def policysearch(request):
    dstaddr = request.GET.get("dstaddr")
    service = request.GET.get("service")
    srcaddr =request.GET.get("srcaddr")

    if not dstaddr and  not srcaddr:
        return render(request, 'policysearch.html')
    else:
        if not srcaddr:
            srcaddr = "0.0.0.0/0"
        if not dstaddr:
            dstaddr = "0.0.0.0/0"
        if not service:
            service = "any"
        policydiclist = []
        searchpolicydic = searchpolicy(topology,netaddrlist,srcaddr,dstaddr,service)
        for j in firewalllist:

            if j.name in searchpolicydic:
                policy =searchpolicydic[j.name]
                for k in policy:
                    policydic = {"dev":j.name,"id": k.name, "srceth": k.srceth, "dsteth": k.dsteth, "srcaddr": k.srcaddr,
                         "dstaddr": k.dstaddr, "service": k.service}
                    policydiclist.append(policydic)
        return JsonResponse({'searchpolicylist': policydiclist})
