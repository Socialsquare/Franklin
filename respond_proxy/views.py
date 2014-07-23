from django.shortcuts import render
from django.http import HttpResponse
import os.path

SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

# Create your views here.
def respond_proxy_js(request):
	file_path = "%s/static/respond_proxy/respond.proxy.js" % SITE_ROOT
	file_data = open(file_path, "rb").read()
	return HttpResponse(file_data, mimetype="application/javascript")

# Create your views here.
def respond_proxy_gif(request):
	file_path = "%s/static/respond_proxy/respond.proxy.gif" % SITE_ROOT
	file_data = open(file_path, "rb").read()
	return HttpResponse(file_data, mimetype="image/gif")