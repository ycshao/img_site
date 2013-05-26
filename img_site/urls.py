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
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('img_site.views',
    # url(r'^$', 'img_site.views.home', name='home'),
)
		
urlpatterns += patterns('img_site.img_uploader.views',
	url(r'^$', 'img_list'),
	url(r'^imgs/$', 'img_list'),
	url(r'^videos/$', 'video_list'),
	url(r'^upload/$', 'upload'),
	url(r'^upload_multi_imgs/$', 'upload_multi_imgs'),
	url(r'^img_detail/([^\s]+)$', 'img_detail'),
	url(r'^video_detail/([^\s]+)$', 'video_detail'),
)
