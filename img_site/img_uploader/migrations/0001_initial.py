# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PictureFile'
        db.create_table(u'img_uploader_picturefile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('picFile', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'img_uploader', ['PictureFile'])


    def backwards(self, orm):
        # Deleting model 'PictureFile'
        db.delete_table(u'img_uploader_picturefile')


    models = {
        u'img_uploader.picturefile': {
            'Meta': {'object_name': 'PictureFile'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'picFile': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['img_uploader']