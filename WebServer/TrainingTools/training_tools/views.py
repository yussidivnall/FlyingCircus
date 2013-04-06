#from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.shortcuts import render_to_response,redirect
from django.core.context_processors import csrf
from django.template import RequestContext
from django import forms

def start_page(request):
    return render_to_response('training_tools/start_page.html')
def new_dataset(request):
    return render_to_response('training_tools/start_page.html')
def new_group(request):
    return render_to_response('training_tools/start_page.html')
def new_person(request):
    return render_to_response('training_tools/start_page.html')

def list_groups(request):
    return render_to_response('training_tools/start_page.html')
def list_pepole(request):
    return render_to_response('training_tools/start_page.html')

def upload_group_images(request):
    return render_to_response('training_tools/start_page.html')
def upload_person_images(request):
    return render_to_response('training_tools/start_page.html')
def upload_video(request):
    return render_to_response('training_tools/start_page.html')
    

