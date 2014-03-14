# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'UserInfo.user'
        db.add_column('global_change_lab_userinfo', 'user',
                      self.gf('django.db.models.fields.related.OneToOneField')(to=orm['global_change_lab.User'], unique=True, null=True, blank=True),
                      keep_default=False)


        # Changing field 'UserInfo.organization'
        db.alter_column('global_change_lab_userinfo', 'organization', self.gf('django.db.models.fields.CharField')(null=True, max_length=140))

        # Changing field 'UserInfo.country'
        db.alter_column('global_change_lab_userinfo', 'country', self.gf('django.db.models.fields.CharField')(null=True, max_length=140))

        # Changing field 'UserInfo.birthdate'
        db.alter_column('global_change_lab_userinfo', 'birthdate', self.gf('django.db.models.fields.DateField')(null=True))
        # Deleting field 'User.userinfo'
        db.delete_column('global_change_lab_user', 'userinfo_id')


    def backwards(self, orm):
        # Deleting field 'UserInfo.user'
        db.delete_column('global_change_lab_userinfo', 'user_id')


        # User chose to not deal with backwards NULL issues for 'UserInfo.organization'
        raise RuntimeError("Cannot reverse this migration. 'UserInfo.organization' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'UserInfo.organization'
        db.alter_column('global_change_lab_userinfo', 'organization', self.gf('django.db.models.fields.CharField')(max_length=140))

        # User chose to not deal with backwards NULL issues for 'UserInfo.country'
        raise RuntimeError("Cannot reverse this migration. 'UserInfo.country' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'UserInfo.country'
        db.alter_column('global_change_lab_userinfo', 'country', self.gf('django.db.models.fields.CharField')(max_length=140))

        # User chose to not deal with backwards NULL issues for 'UserInfo.birthdate'
        raise RuntimeError("Cannot reverse this migration. 'UserInfo.birthdate' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'UserInfo.birthdate'
        db.alter_column('global_change_lab_userinfo', 'birthdate', self.gf('django.db.models.fields.DateField')())

        # User chose to not deal with backwards NULL issues for 'User.userinfo'
        raise RuntimeError("Cannot reverse this migration. 'User.userinfo' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'User.userinfo'
        db.add_column('global_change_lab_user', 'userinfo',
                      self.gf('django.db.models.fields.related.OneToOneField')(to=orm['global_change_lab.UserInfo'], unique=True),
                      keep_default=False)


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'ordering': "('name',)", 'db_table': "'django_content_type'", 'object_name': 'ContentType'},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'global_change_lab.siteconfiguration': {
            'Meta': {'object_name': 'SiteConfiguration'},
            'analytics_code': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'global_change_lab.user': {
            'Meta': {'object_name': 'User'},
            'datetime_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'related_name': "'user_set'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'null': 'True', 'max_length': '100', 'blank': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'skills_completed': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['skills.Skill']", 'symmetrical': 'False', 'related_name': "'users_completed'", 'blank': 'True'}),
            'skills_in_progress': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['skills.Skill']", 'symmetrical': 'False', 'related_name': "'users_in_progress'", 'blank': 'True'}),
            'trainingbits_completed': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['skills.TrainingBit']", 'symmetrical': 'False', 'related_name': "'users_completed'", 'blank': 'True'}),
            'trainingbits_in_progress': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['skills.TrainingBit']", 'symmetrical': 'False', 'related_name': "'users_in_progress'", 'blank': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'related_name': "'user_set'", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'})
        },
        'global_change_lab.userinfo': {
            'Meta': {'object_name': 'UserInfo'},
            'birthdate': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '140'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organization': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '140'}),
            'sex': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['global_change_lab.User']", 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        'skills.skill': {
            'Meta': {'object_name': 'Skill'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['global_change_lab.User']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'trainingbits': ('sortedm2m.fields.SortedManyToManyField', [], {'to': "orm['skills.TrainingBit']", 'symmetrical': 'False', 'blank': 'True'}),
            'updated_at': ('skills.models.AutoDateTimeField', [], {})
        },
        'skills.trainingbit': {
            'Meta': {'ordering': "['-created_at']", 'object_name': 'TrainingBit'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['global_change_lab.User']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'is_draft': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'json_content': ('django.db.models.fields.TextField', [], {'default': '\'{"learn":[],"act":[],"share":[]}\''}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'recommended': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'updated_at': ('skills.models.AutoDateTimeField', [], {})
        }
    }

    complete_apps = ['global_change_lab']