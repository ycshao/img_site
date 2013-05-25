from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
#from django.views.decorators.csrf import csrf_exempt
from django import forms
from img_site.img_uploader.models import PictureFile
from img_site.settings import *
import pdb

class  UploadFileForm(forms.Form):
	title = forms.CharField(max_length=50)
	file = forms.FileField(label='Select a picture',help_text=r"No larger than 2MB please.")

#f is request.FILES['file']
def save_upload_file(f):
	#f.read() 
	#f.name()
	#f.size()
	destination = open(IMG_UPLOAD_PATH + f.name, 'wb+')
	for chunk in f.chunks():
		destination.write(chunk)
	destination.close()

def multiple_upload(request):
	"""docstring for multiple_upload"""
	for	f in request.FILES.getlist('file'):
		save_upload_file(f)
		
def upload(request):
	c = {}
	c.update(csrf(request))
	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():
			f = request.FILES['file'];
			f.name.replace(' ', '_');
			save_upload_file(f)
			new_img = PictureFile(picFile=f, title=request.POST['title'])
			new_img.save()
			#redirect_url = IMG_UPLOAD_URL + request.FILES['file'].name
			redirect_url = '/img_detail/%s' % new_img.id
			#return HttpResponse(redirect_url)
			return HttpResponseRedirect(redirect_url)
		else:
			return HttpResponse("form is not valid")
		#if 'img_file' in request.POST:
			#imgfile = request.POST['img_file']
	else:
		form = UploadFileForm()
		c['form'] = form
		return render_to_response('upload_img.html', c)
	
def video_list(request):
	all_objs = PictureFile.objects.all()
	video_objs = []
	for obj in all_objs:
		path, ext = os.path.splitext(obj.picFile.name)
		if ext in ['.avi','.mp4','.rmvb','.m4v', '.mov', '.wmv', '.mpeg']:
			video_objs.append(obj)
	return render_to_response('video_list.html', {'videos':video_objs, 'video_dir':MEDIA_URL})

def img_list(request):
	all_objs = PictureFile.objects.all()
	photo_objs = []
	for obj in all_objs:
		path, ext = os.path.splitext(obj.picFile.name)
		if ext in ['.jpg','.jpeg','.gif','.bmp']:
			photo_objs.append(obj)
	return render_to_response('img_list.html', {'photos':photo_objs, 'img_dir': MEDIA_URL})
	
def img_detail(request, img_id):
	#to retrieve single object
	try:
		photo = PictureFile.objects.get(id=img_id)
		return render_to_response('img_detail.html', {'photo':photo, 'img_dir':MEDIA_URL})
	except PictureFile.DoesNotExist:
		return HttpResponseRedirect(r"/404.html")

def video_detail(request, video_id):
	#to retrieve single object
	try:
		video = PictureFile.objects.get(id=video_id)
		return render_to_response('video_detail.html', {'video':video, 'video_dir': MEDIA_URL})
	except PictureFile.DoesNotExist:
		return HttpResponseRedirect(r"/404.html")
