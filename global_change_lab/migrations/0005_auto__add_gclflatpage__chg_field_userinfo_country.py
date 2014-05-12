# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'GCLFlatPage'
        db.create_table('global_change_lab_gclflatpage', (
            ('flatpage_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['flatpages.FlatPage'], primary_key=True, unique=True)),
            ('show_in_footer', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('global_change_lab', ['GCLFlatPage'])


        # Changing field 'UserInfo.country'
        db.alter_column('global_change_lab_userinfo', 'country', self.gf('django_countries.fields.CountryField')(null=True, max_length=2))

    def backwards(self, orm):
        # Deleting model 'GCLFlatPage'
        db.delete_table('global_change_lab_gclflatpage')


        # Changing field 'UserInfo.country'
        db.alter_column('global_change_lab_userinfo', 'country', self.gf('django.db.models.fields.CharField')(null=True, max_length=140))

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['auth.Permission']", 'symmetrical': 'False'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission', 'ordering': "('content_type__app_label', 'content_type__model', 'codename')"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'contenttypes.contenttype': {
            'Meta': {'db_table': "'django_content_type'", 'object_name': 'ContentType', 'unique_together': "(('app_label', 'model'),)", 'ordering': "('name',)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'flatpages.flatpage': {
            'Meta': {'db_table': "'django_flatpage'", 'object_name': 'FlatPage', 'ordering': "('url',)"},
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'enable_comments': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'registration_required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['sites.Site']", 'symmetrical': 'False'}),
            'template_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '70'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'url': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '100'})
        },
        'global_change_lab.gclflatpage': {
            'Meta': {'_ormbases': ['flatpages.FlatPage'], 'object_name': 'GCLFlatPage', 'ordering': "('url',)"},
            'flatpage_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['flatpages.FlatPage']", 'primary_key': 'True', 'unique': 'True'}),
            'show_in_footer': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
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
            'email': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '100'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['auth.Group']", 'symmetrical': 'False', 'related_name': "'user_set'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'blank': 'True', 'null': 'True', 'max_length': '100'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'skills_completed': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['skills.Skill']", 'symmetrical': 'False', 'related_name': "'users_completed'"}),
            'skills_in_progress': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['skills.Skill']", 'symmetrical': 'False', 'related_name': "'users_in_progress'"}),
            'trainingbits_completed': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['skills.TrainingBit']", 'symmetrical': 'False', 'related_name': "'users_completed'"}),
            'trainingbits_in_progress': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['skills.TrainingBit']", 'symmetrical': 'False', 'related_name': "'users_in_progress'"}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['auth.Permission']", 'symmetrical': 'False', 'related_name': "'user_set'"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'})
        },
        'global_change_lab.userinfo': {
            'Meta': {'object_name': 'UserInfo'},
            'birthdate': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'country': ('django_countries.fields.CountryField', [], {'null': 'True', 'max_length': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organization': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'sex': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'to': "orm['global_change_lab.User']", 'null': 'True', 'unique': 'True'})
        },
        'sites.site': {
            'Meta': {'db_table': "'django_site'", 'object_name': 'Site', 'ordering': "('domain',)"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'skills.skill': {
            'Meta': {'object_name': 'Skill'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['global_change_lab.User']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_draft': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_recommended': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '60'}),
            'trainingbits': ('sortedm2m.fields.SortedManyToManyField', [], {'blank': 'True', 'to': "orm['skills.TrainingBit']", 'symmetrical': 'False'}),
            'updated_at': ('skills.models.AutoDateTimeField', [], {})
        },
        'skills.trainingbit': {
            'Meta': {'object_name': 'TrainingBit', 'ordering': "['-created_at']"},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['global_change_lab.User']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'blank': 'True', 'max_length': '100'}),
            'is_draft': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_recommended': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'json_content': ('django.db.models.fields.TextField', [], {'default': '\'{"learn":[],"act":[],"share":[]}\''}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '60'}),
            'updated_at': ('skills.models.AutoDateTimeField', [], {})
        }
    }

    complete_apps = ['global_change_lab']