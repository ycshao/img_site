from django.db import models

# Create your models here.
class PictureFile(models.Model):
	picFile = models.FileField(upload_to='upload/')
	title = models.CharField(max_length=255)
	
	def __unicode__(self):
		return '%s (%s)' % (self.title, self.picFile)
	
