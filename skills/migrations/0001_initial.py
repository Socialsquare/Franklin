# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Like'
        db.create_table('skills_like', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('updated_at', self.gf('skills.models.AutoDateTimeField')()),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('skills', ['Like'])

        # Adding model 'Image'
        db.create_table('skills_image', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('updated_at', self.gf('skills.models.AutoDateTimeField')()),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('identifier', self.gf('django.db.models.fields.CharField')(max_length=36)),
        ))
        db.send_create_signal('skills', ['Image'])

        # Adding model 'TrainingBit'
        db.create_table('skills_trainingbit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('updated_at', self.gf('skills.models.AutoDateTimeField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('json_content', self.gf('django.db.models.fields.TextField')(default='{"learn":[],"act":[],"share":[]}')),
            ('recommended', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_draft', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('skills', ['TrainingBit'])

        # Adding model 'Project'
        db.create_table('skills_project', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('updated_at', self.gf('skills.models.AutoDateTimeField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('link', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('video', self.gf('embed_video.fields.EmbedVideoField')(max_length=200, blank=True, null=True)),
            ('trainingbit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['skills.TrainingBit'])),
            ('is_public', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('skills', ['Project'])

        # Adding model 'Comment'
        db.create_table('skills_comment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('updated_at', self.gf('skills.models.AutoDateTimeField')()),
            ('text', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['skills.Project'])),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['skills.Comment'])),
            ('is_flagged', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_hidden', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('skills', ['Comment'])

        # Adding model 'Skill'
        db.create_table('skills_skill', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('updated_at', self.gf('skills.models.AutoDateTimeField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('is_public', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('skills', ['Skill'])


        # Adding SortedM2M table for field trainingbits on 'Skill'
        db.create_table('skills_skill_trainingbits', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('skill', models.ForeignKey(orm['skills.skill'], null=False)),
            ('trainingbit', models.ForeignKey(orm['skills.trainingbit'], null=False)),
            ('sort_value', models.IntegerField())
        ))
        db.create_unique('skills_skill_trainingbits', ['skill_id', 'trainingbit_id'])
        # Adding model 'Topic'
        db.create_table('skills_topic', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('updated_at', self.gf('skills.models.AutoDateTimeField')()),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('slug', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
        ))
        db.send_create_signal('skills', ['Topic'])

        # Adding M2M table for field trainingbits on 'Topic'
        m2m_table_name = db.shorten_name('skills_topic_trainingbits')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('topic', models.ForeignKey(orm['skills.topic'], null=False)),
            ('trainingbit', models.ForeignKey(orm['skills.trainingbit'], null=False))
        ))
        db.create_unique(m2m_table_name, ['topic_id', 'trainingbit_id'])

        # Adding M2M table for field skills on 'Topic'
        m2m_table_name = db.shorten_name('skills_topic_skills')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('topic', models.ForeignKey(orm['skills.topic'], null=False)),
            ('skill', models.ForeignKey(orm['skills.skill'], null=False))
        ))
        db.create_unique(m2m_table_name, ['topic_id', 'skill_id'])


    def backwards(self, orm):
        # Deleting model 'Like'
        db.delete_table('skills_like')

        # Deleting model 'Image'
        db.delete_table('skills_image')

        # Deleting model 'TrainingBit'
        db.delete_table('skills_trainingbit')

        # Deleting model 'Project'
        db.delete_table('skills_project')

        # Deleting model 'Comment'
        db.delete_table('skills_comment')

        # Deleting model 'Skill'
        db.delete_table('skills_skill')

        # Removing M2M table for field trainingbits on 'Skill'
        db.delete_table(db.shorten_name('skills_skill_trainingbits'))

        # Deleting model 'Topic'
        db.delete_table('skills_topic')

        # Removing M2M table for field trainingbits on 'Topic'
        db.delete_table(db.shorten_name('skills_topic_trainingbits'))

        # Removing M2M table for field skills on 'Topic'
        db.delete_table(db.shorten_name('skills_topic_skills'))


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['auth.Permission']"})
        },
        'auth.permission': {
            'Meta': {'object_name': 'Permission', 'unique_together': "(('content_type', 'codename'),)", 'ordering': "('content_type__app_label', 'content_type__model', 'codename')"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'contenttypes.contenttype': {
            'Meta': {'object_name': 'ContentType', 'unique_together': "(('app_label', 'model'),)", 'ordering': "('name',)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'skills.comment': {
            'Meta': {'object_name': 'Comment'},
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
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'updated_at': ('skills.models.AutoDateTimeField', [], {})
        },
        'skills.like': {
            'Meta': {'object_name': 'Like'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'updated_at': ('skills.models.AutoDateTimeField', [], {})
        },
        'skills.project': {
            'Meta': {'object_name': 'Project'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'trainingbit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['skills.TrainingBit']"}),
            'updated_at': ('skills.models.AutoDateTimeField', [], {}),
            'video': ('embed_video.fields.EmbedVideoField', [], {'max_length': '200', 'blank': 'True', 'null': 'True'})
        },
        'skills.skill': {
            'Meta': {'object_name': 'Skill'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'trainingbits': ('sortedm2m.fields.SortedManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['skills.TrainingBit']"}),
            'updated_at': ('skills.models.AutoDateTimeField', [], {})
        },
        'skills.topic': {
            'Meta': {'object_name': 'Topic'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'skills': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['skills.Skill']"}),
            'slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'trainingbits': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['skills.TrainingBit']"}),
            'updated_at': ('skills.models.AutoDateTimeField', [], {})
        },
        'skills.trainingbit': {
            'Meta': {'object_name': 'TrainingBit', 'ordering': "['-created_at']"},
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

    complete_apps = ['skills']
