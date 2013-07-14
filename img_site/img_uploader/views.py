from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
#from django.views.decorators.csrf import csrf_exempt
from django import forms
from img_site.img_uploader.models import PictureFile
from img_site.settings import *
from img_site.img_uploader.image_utils import *
import random
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

def select_imgs(request):
	all_objs = PictureFile.objects.all()
	photos_col = []
	i=0
	for obj in all_objs:
		path, ext = os.path.splitext(obj.picFile.name)
		if is_img_type(ext):
			photos_col.append(obj)
	c = {'photos_col':photos_col, 'img_dir': MEDIA_URL}
	c.update(csrf(request))
	return render_to_response('select_imgs.html', c)

def get_rand_str(n): 
	al=list('abcdefghijklmnopqrstuvwxyz') 
	list_len = len(al)
	str='' 
	for i in range(n): 
		index = random.randint(0,list_len - 1) 
		str = str + al[index] 
	return str

def make_gif(request):
	if request.method == 'POST':
		selected_items = request.POST.getlist('selected_items')  
		paths = []
		for img_id in selected_items:
			photo = PictureFile.objects.get(id=img_id)
			paths.append(photo.picFile.path)	
		output_filename = get_rand_str(8) + '.gif'
		output_path = GIF_DIR + output_filename
		output_url = r'/media/gif/' + output_filename
		sortAndCombineImgsToGif(output_path, paths)
		return HttpResponseRedirect(r'/gif_detail/%s' % output_filename)
		
def gif_detail(request, filename):
	c = {'filename':filename, 'gif_dir':GIF_URL}
	c.update(csrf(request))
	return render_to_response('gif_detail.html', c)