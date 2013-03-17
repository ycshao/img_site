from django.db import models

# Create your models here.
class PictureFile(models.Model):
	picFile = models.FileField(upload_to='upload/')
	
