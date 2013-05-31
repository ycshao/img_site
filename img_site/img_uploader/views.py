from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
#from django.views.decorators.csrf import csrf_exempt
from django import forms
from img_site.img_uploader.models import PictureFile
from img_site.settings import *
import pdb

def get_media_type(ext):
	'''
	1: picture type
	2: video type
	0: not supported
	'''
	if ext.lower() in ['.jpg','.jpeg','.gif','.bmp']:
		return 1
	elif ext.lower() in ['.avi','.mp4','.rmvb','.m4v', '.wmv', '.mpeg']:
		return 2
	else:
		return 0
	
def is_video_type(ext):
	return get_media_type(ext) == 2
	
def is_img_type(ext):
	return get_media_type(ext) == 1
	
#f is request.FILES['file']
def save_upload_file(f):
	#f.read()
	#f.name()
	#f.size()
	destination = open(IMG_UPLOAD_PATH + f.name, 'wb+')
	for chunk in f.chunks():
		destination.write(chunk)
	destination.close()

def upload_multi_imgs(request):
	"""docstring for multiple_upload"""
	c = {}
	c.update(csrf(request))
	if request.method == 'POST':
		for	f in request.FILES.getlist('multi_file_field'):
			f.name.replace(' ', '_');
			save_upload_file(f)
			path, ext = os.path.splitext(f.name)
			path, filename = os.path.split(path)
			new_img = PictureFile(picFile=f, title=filename)
			new_img.save()
		return HttpResponseRedirect('/imgs/')
	else:
		return render_to_response('upload_multi_imgs.html', c)
		
def upload(request):
	c = {}
	c.update(csrf(request))
	if request.method == 'POST':
		f = request.FILES['file_field'];
		f.name.replace(' ', '_');
		save_upload_file(f)
		new_img = PictureFile(picFile=f, title=request.POST['title'])
		new_img.save()
		path, ext = os.path.splitext(f.name)
		redirect_url = ''
		if is_img_type(ext):
			redirect_url = '/img_detail/%s' % new_img.id
		elif is_video_type(ext):
			redirect_url = '/video_detail/%s' % new_img.id
		#redirect_url = IMG_UPLOAD_URL + request.FILES['file'].name	
		#return HttpResponse(redirect_url)
		return HttpResponseRedirect(redirect_url)
	else:
		return render_to_response('upload.html', c)

def video_list(request):
	all_objs = PictureFile.objects.all()
	video_objs = []
	for obj in all_objs:
		path, ext = os.path.splitext(obj.picFile.name)
		if is_video_type(ext):
			video_objs.append(obj)
	return render_to_response('video_list.html', {'videos':video_objs, 'video_dir':MEDIA_URL})

def img_list(request):
	all_objs = PictureFile.objects.all()
	photos_col1 = []
	photos_col2 = []
	photos_col3 = []
	i=0
	for obj in all_objs:
		path, ext = os.path.splitext(obj.picFile.name)
		if is_img_type(ext):
			if i%3 == 0:
				photos_col1.append(obj)
			elif i%2 == 1:
				photos_col2.append(obj)
			else:
				photos_col3.append(obj)
			i = i + 1
	return render_to_response('img_list.html', {'photos_col1':photos_col1, 
												'photos_col2':photos_col2,
												'photos_col3': photos_col3, 
												'img_dir': MEDIA_URL})
	
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
