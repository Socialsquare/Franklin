# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):
    depends_on = (
        ('skills', '0001_initial'),
    )

    def forwards(self, orm):
        # Adding model 'UserInfo'
        db.create_table('global_change_lab_userinfo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sex', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('birthdate', self.gf('django.db.models.fields.DateField')()),
            ('organization', self.gf('django.db.models.fields.CharField')(max_length=140)),
        ))
        db.send_create_signal('global_change_lab', ['UserInfo'])

        # Adding model 'User'
        db.create_table('global_change_lab_user', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('is_superuser', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('datetime_joined', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('username', self.gf('django.db.models.fields.CharField')(unique=True, max_length=40)),
            ('email', self.gf('django.db.models.fields.CharField')(blank=True, max_length=100)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(null=True, blank=True, max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('userinfo', self.gf('django.db.models.fields.related.OneToOneField')(unique=True, to=orm['global_change_lab.UserInfo'])),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('global_change_lab', ['User'])

        # Adding M2M table for field groups on 'User'
        m2m_table_name = db.shorten_name('global_change_lab_user_groups')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('user', models.ForeignKey(orm['global_change_lab.user'], null=False)),
            ('group', models.ForeignKey(orm['auth.group'], null=False))
        ))
        db.create_unique(m2m_table_name, ['user_id', 'group_id'])

        # Adding M2M table for field user_permissions on 'User'
        m2m_table_name = db.shorten_name('global_change_lab_user_user_permissions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('user', models.ForeignKey(orm['global_change_lab.user'], null=False)),
            ('permission', models.ForeignKey(orm['auth.permission'], null=False))
        ))
        db.create_unique(m2m_table_name, ['user_id', 'permission_id'])

        # Adding M2M table for field skills_in_progress on 'User'
        m2m_table_name = db.shorten_name('global_change_lab_user_skills_in_progress')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('user', models.ForeignKey(orm['global_change_lab.user'], null=False)),
            ('skill', models.ForeignKey(orm['skills.skill'], null=False))
        ))
        db.create_unique(m2m_table_name, ['user_id', 'skill_id'])

        # Adding M2M table for field skills_completed on 'User'
        m2m_table_name = db.shorten_name('global_change_lab_user_skills_completed')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('user', models.ForeignKey(orm['global_change_lab.user'], null=False)),
            ('skill', models.ForeignKey(orm['skills.skill'], null=False))
        ))
        db.create_unique(m2m_table_name, ['user_id', 'skill_id'])

        # Adding M2M table for field trainingbits_in_progress on 'User'
        m2m_table_name = db.shorten_name('global_change_lab_user_trainingbits_in_progress')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('user', models.ForeignKey(orm['global_change_lab.user'], null=False)),
            ('trainingbit', models.ForeignKey(orm['skills.trainingbit'], null=False))
        ))
        db.create_unique(m2m_table_name, ['user_id', 'trainingbit_id'])

        # Adding M2M table for field trainingbits_completed on 'User'
        m2m_table_name = db.shorten_name('global_change_lab_user_trainingbits_completed')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('user', models.ForeignKey(orm['global_change_lab.user'], null=False)),
            ('trainingbit', models.ForeignKey(orm['skills.trainingbit'], null=False))
        ))
        db.create_unique(m2m_table_name, ['user_id', 'trainingbit_id'])

        # Adding model 'SiteConfiguration'
        db.create_table('global_change_lab_siteconfiguration', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('analytics_code', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('global_change_lab', ['SiteConfiguration'])


    def backwards(self, orm):
        # Deleting model 'UserInfo'
        db.delete_table('global_change_lab_userinfo')

        # Deleting model 'User'
        db.delete_table('global_change_lab_user')

        # Removing M2M table for field groups on 'User'
        db.delete_table(db.shorten_name('global_change_lab_user_groups'))

        # Removing M2M table for field user_permissions on 'User'
        db.delete_table(db.shorten_name('global_change_lab_user_user_permissions'))

        # Removing M2M table for field skills_in_progress on 'User'
        db.delete_table(db.shorten_name('global_change_lab_user_skills_in_progress'))

        # Removing M2M table for field skills_completed on 'User'
        db.delete_table(db.shorten_name('global_change_lab_user_skills_completed'))

        # Removing M2M table for field trainingbits_in_progress on 'User'
        db.delete_table(db.shorten_name('global_change_lab_user_trainingbits_in_progress'))

        # Removing M2M table for field trainingbits_completed on 'User'
        db.delete_table(db.shorten_name('global_change_lab_user_trainingbits_completed'))

        # Deleting model 'SiteConfiguration'
        db.delete_table('global_change_lab_siteconfiguration')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['auth.Permission']"})
        },
        'auth.permission': {
            'Meta': {'object_name': 'Permission', 'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'contenttypes.contenttype': {
            'Meta': {'object_name': 'ContentType', 'db_table': "'django_content_type'", 'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)"},
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
            'email': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '100'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'symmetrical': 'False', 'blank': 'True', 'to': "orm['auth.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'null': 'True', 'blank': 'True', 'max_length': '100'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'skills_completed': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'users_completed'", 'symmetrical': 'False', 'blank': 'True', 'to': "orm['skills.Skill']"}),
            'skills_in_progress': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'users_in_progress'", 'symmetrical': 'False', 'blank': 'True', 'to': "orm['skills.Skill']"}),
            'trainingbits_completed': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'users_completed'", 'symmetrical': 'False', 'blank': 'True', 'to': "orm['skills.TrainingBit']"}),
            'trainingbits_in_progress': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'users_in_progress'", 'symmetrical': 'False', 'blank': 'True', 'to': "orm['skills.TrainingBit']"}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'symmetrical': 'False', 'blank': 'True', 'to': "orm['auth.Permission']"}),
            'userinfo': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['global_change_lab.UserInfo']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'})
        },
        'global_change_lab.userinfo': {
            'Meta': {'object_name': 'UserInfo'},
            'birthdate': ('django.db.models.fields.DateField', [], {}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organization': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'sex': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'skills.skill': {
            'Meta': {'object_name': 'Skill'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['global_change_lab.User']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'trainingbits': ('sortedm2m.fields.SortedManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['skills.TrainingBit']"}),
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
            'json_content': ('django.db.models.fields.TextField', [], {'default': '\'{"learn":[],"act":[],"share":[]}\''}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'recommended': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'updated_at': ('skills.models.AutoDateTimeField', [], {})
        }
    }

    complete_apps = ['global_change_lab']
