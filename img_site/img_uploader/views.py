# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
#from django.views.decorators.csrf import csrf_exempt
from django import forms
from img_site.img_uploader.models import PictureFile
from img_site.settings import *

class  UploadFileForm(forms.Form):
	title = forms.CharField(max_length=50)
	file = forms.FileField(label='Select a picture',help_text=r"No larger than 2MB please.")

#f is request.FILES['file']
def save_upload_file(f):
	#f.read() 
	#f.name()
	#f.size()
	uploadPath = MEDIA_ROOT + '/upload/'
	destination = open(uploadPath+f.name.replace(' ', '_'), 'wb+')
	for chunk in f.chunks():
		destination.write(chunk)
	destination.close()
	
def upload(request):
	c = {}
	c.update(csrf(request))
	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():
			save_upload_file(request.FILES['file'])
			picDoc = PictureFile(picFile=request.FILES['file'].name.replace(' ', '_'), title=request.POST['title'])
			picDoc.save()
			file_url = '/media/upload/' + request.FILES['file'].name.replace(' ', '_')
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
	
def img_list(request):
	photo_objs = PictureFile.objects.all()
	path = '/media/'
	return render_to_response('img_list.html', {'photos':photo_objs, 'path': path})

def img_detail(request, img_title):
	#photos = PictureFile.objects.filter(title=img_title)
	#photos = PictureFile.objects.filter(title__contains=img_title)
	
	#to retrieve single object
	photo = PictureFile.objects.get(title=img_title)
	if photo:
		file_url = "/media/" + str(photo.picFile)
		return HttpResponseRedirect(file_url)
	else:
		return HttpResponseRedirect("/404.html")
