from django.shortcuts import render
from django.http import HttpResponse
from confmgrweb.settings import *

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
    return  render(request,'policytab.html',{'firewalllist':firewalllist})
