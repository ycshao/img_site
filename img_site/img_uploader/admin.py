from django.contrib import admin
from img_site.img_uploader.models import PictureFile

class PictureFileAdmin(admin.ModelAdmin):
    list_display = ('title', 'picFile')

admin.site.register(PictureFile, PictureFileAdmin)
