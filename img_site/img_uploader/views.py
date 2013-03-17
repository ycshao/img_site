# Create your views here.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
#from django.views.decorators.csrf import csrf_exempt
from django import forms
from img_site.img_uploader.models import PictureFile

class  UploadFileForm(forms.Form):
	title = forms.CharField(max_length=50)
	file = forms.FileField(label='Select a picture', help_text='max. 42 megatbytes')


def upload(request):
	c = {}
	c.update(csrf(request))
	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():
			picDoc = PictureFile(picFile=request.FILES['file'])
			picDoc.save()
			file_url = '/media/upload/' + request.FILES['file'].name
			#return HttpResponse(file_url)
			return HttpResponseRedirect(file_url)
		else:
			return HttpResponse("form is not valid")
		#if 'img_file' in request.POST:
			#imgfile = request.POST['img_file']
	else:
		form = UploadFileForm()
		c['form'] = form
		return render_to_response('upload_img.html', c)
		
def display_img(request):
	return HttpResponseRedirect('/media/sample.JPG') #for test
	
