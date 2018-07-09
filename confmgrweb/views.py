from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from confmgrweb.settings import *
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
                    print(policydiclist)

                    return JsonResponse({'policydic':policydiclist})
                elif policytype == 'policydetaillist':
                    return HttpResponse(  i.policydetaillist)
                elif policytype == 'policymiclist':
                    return HttpResponse(i.policymiclist)

