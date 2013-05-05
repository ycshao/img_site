from django.conf.urls import patterns, include, url
from django.views.static import *
from django.conf import settings
from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:

	# required to make static serving work
	(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^static/admin/(?P<path>.*)$', 'django.views.static.serve', {'document_root':settings.ADMIN_STATIC_ROOT}),
)

urlpatterns += patterns('img_site.views',
    # url(r'^$', 'img_site.views.home', name='home'),
)
#URL map:
#/			home page		
#/upload	upload user's own image/video
#			
urlpatterns += patterns('img_site.img_uploader.views',
	url(r'^$', 'upload'),
	url(r'^upload$', 'upload'),
	url(r'^display$', 'display_img'),
	url(r'^img_list$', 'img_list'),
	url(r'^img_list/([^\s]+)$', 'img_detail'),
)
