from django.shortcuts import render
from django.http import HttpResponse
from .SolarEdge import *

# Create your views here.

def home(request):
    unit1_data = unit1()
    unit2_data = unit2()
    all_data = all(unit1_data, unit2_data)
    context = {'unit1': unit1_data, 'unit2': unit2_data, 'all_data': all_data}
    return render(request, 'Dashboard/home.html', context)
