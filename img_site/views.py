from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
#from django.views.decorators.csrf import csrf_exempt
from django import forms


#@csrf_exempt
def home(request):
	return HttpResponse("Hello")
