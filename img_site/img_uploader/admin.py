from django.contrib import admin
from img_site.img_uploader.models import PictureFile

class PictureFileAdmin(admin.ModelAdmin):
	list_display = ('title','picFile',)
	list_filter = ('title',)
	ordering = ('-title',) 
	fields = ('title', 'picFile') # control the editable date fields, in this case, publication_date is not editable
	
admin.site.register(PictureFile, PictureFileAdmin)
