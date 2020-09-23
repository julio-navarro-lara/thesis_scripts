# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
from django.shortcuts import render, render_to_response
from django.views.generic import TemplateView

from django.http import HttpResponse, JsonResponse

from django.conf import settings

from utils.create_graph import main_create_graph
from utils.create_graph import main_extract_logs
from utils.previous_stats import main_calculate_previous_stats

import json
# Create your views here.

class MainView(TemplateView):
    template_name = "index.html"

class SimscAutoView(TemplateView):
    template_name = "simsc_auto.html"

def generate_graph(request):
    n_commonip = request.POST.get('n_commonip', '1')
    n_timedif = request.POST.get('n_timedif', '6')
    file = request.FILES['log_file']
    handle_uploaded_file(file)

    list_logs_dict = main_extract_logs()

    length_nodes = main_create_graph(list_logs_dict,n_commonip,n_timedif)
    return render(request, 'graph.html', {})

def generate_stats(request):

    n_commonip = request.POST.get('n_commonip', '1')
    n_timedif = request.POST.get('n_timedif', '6')
    file = request.FILES['log_file']
    handle_uploaded_file(file)

    list_logs_dict = main_extract_logs()

    main_calculate_previous_stats(list_logs_dict,n_timedif,n_commonip)
    return render(request, 'stats_graph.html', {})

def data_graph(request):
	file_json = open('utils/data/graph_ip.json')
	json_response = json.load(file_json) #They are pairs [date, value], and the date has to be given in millisecond
	#json_response[0][1]=100*random.random()
	return JsonResponse(json_response, safe=False)

def handle_uploaded_file(f):
    with open('utils/data/list_logs.csv', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
