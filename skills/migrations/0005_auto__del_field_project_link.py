# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Project.link'
        db.delete_column('skills_project', 'link')


    def backwards(self, orm):
        # Adding field 'Project.link'
        db.add_column('skills_project', 'link',
                      self.gf('django.db.models.fields.URLField')(blank=True, max_length=200, default=''),
                      keep_default=False)


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['auth.Permission']", 'symmetrical': 'False'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'contenttypes.contenttype': {
            'Meta': {'db_table': "'django_content_type'", 'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType'},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'global_change_lab.user': {
            'Meta': {'object_name': 'User'},
            'datetime_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '100'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'blank': 'True', 'to': "orm['auth.Group']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'null': 'True', 'blank': 'True', 'max_length': '100'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'skills_completed': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'users_completed'", 'blank': 'True', 'to': "orm['skills.Skill']", 'symmetrical': 'False'}),
            'skills_in_progress': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'users_in_progress'", 'blank': 'True', 'to': "orm['skills.Skill']", 'symmetrical': 'False'}),
            'trainingbits_completed': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'users_completed'", 'blank': 'True', 'to': "orm['skills.TrainingBit']", 'symmetrical': 'False'}),
            'trainingbits_in_progress': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'users_in_progress'", 'blank': 'True', 'to': "orm['skills.TrainingBit']", 'symmetrical': 'False'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'blank': 'True', 'to': "orm['auth.Permission']", 'symmetrical': 'False'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'})
        },
        'skills.comment': {
            'Meta': {'object_name': 'Comment'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['global_change_lab.User']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_flagged': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['skills.Comment']"}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['skills.Project']"}),
            'text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'updated_at': ('skills.models.AutoDateTimeField', [], {})
        },
        'skills.image': {
            'Meta': {'object_name': 'Image'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'uploaded_images'", 'to': "orm['global_change_lab.User']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'blank': 'True', 'max_length': '100'}),
            'updated_at': ('skills.models.AutoDateTimeField', [], {})
        },
        'skills.like': {
            'Meta': {'object_name': 'Like'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['global_change_lab.User']"}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'updated_at': ('skills.models.AutoDateTimeField', [], {})
        },
        'skills.project': {
            'Meta': {'object_name': 'Project'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['global_change_lab.User']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'blank': 'True', 'max_length': '100'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'link_title': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '100'}),
            'link_url': ('django.db.models.fields.URLField', [], {'blank': 'True', 'max_length': '200'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'trainingbit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['skills.TrainingBit']"}),
            'updated_at': ('skills.models.AutoDateTimeField', [], {}),
            'video': ('embed_video.fields.EmbedVideoField', [], {'null': 'True', 'blank': 'True', 'max_length': '200'})
        },
        'skills.skill': {
            'Meta': {'object_name': 'Skill'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['global_change_lab.User']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_draft': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'trainingbits': ('sortedm2m.fields.SortedManyToManyField', [], {'blank': 'True', 'to': "orm['skills.TrainingBit']", 'symmetrical': 'False'}),
            'updated_at': ('skills.models.AutoDateTimeField', [], {})
        },
        'skills.topic': {
            'Meta': {'object_name': 'Topic'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['global_change_lab.User']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'skills': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['skills.Skill']", 'symmetrical': 'False'}),
            'slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'trainingbits': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['skills.TrainingBit']", 'symmetrical': 'False'}),
            'updated_at': ('skills.models.AutoDateTimeField', [], {})
        },
        'skills.trainingbit': {
            'Meta': {'ordering': "['-created_at']", 'object_name': 'TrainingBit'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['global_change_lab.User']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'blank': 'True', 'max_length': '100'}),
            'is_draft': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'json_content': ('django.db.models.fields.TextField', [], {'default': '\'{"learn":[],"act":[],"share":[]}\''}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'recommended': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'updated_at': ('skills.models.AutoDateTimeField', [], {})
        }
    }

    complete_apps = ['skills']