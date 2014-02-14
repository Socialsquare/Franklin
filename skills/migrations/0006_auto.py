# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

def migratedata(orm):
    # copy data, need to lookup model through orm.
    for skill in orm['skills.skill'].objects.all():
        # convert old name to new name
        # "training_bits" -> "trainingbits"
        skill.trainingbits.add(*skill.training_bits.all())
        skill.save()

class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding M2M table for field trainingbits on 'Skill'
        m2m_table_name = db.shorten_name('skills_skill_trainingbits')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('skill', models.ForeignKey(orm['skills.skill'], null=False)),
            ('trainingbit', models.ForeignKey(orm['skills.trainingbit'], null=False))
        ))
        db.create_unique(m2m_table_name, ['skill_id', 'trainingbit_id'])

        # migrate data
        if not db.dry_run:
            migratedata(orm)

        # Removing M2M table for field training_bits on 'Skill'
        db.delete_table(db.shorten_name('skills_skill_training_bits'))



    def backwards(self, orm):
        # Adding M2M table for field training_bits on 'Skill'
        m2m_table_name = db.shorten_name('skills_skill_training_bits')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('skill', models.ForeignKey(orm['skills.skill'], null=False)),
            ('trainingbit', models.ForeignKey(orm['skills.trainingbit'], null=False))
        ))
        db.create_unique(m2m_table_name, ['skill_id', 'trainingbit_id'])

        # Removing M2M table for field trainingbits on 'Skill'
        db.delete_table(db.shorten_name('skills_skill_trainingbits'))


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['auth.Permission']", 'symmetrical': 'False'})
        },
        'auth.permission': {
            'Meta': {'object_name': 'Permission', 'unique_together': "(('content_type', 'codename'),)", 'ordering': "('content_type__app_label', 'content_type__model', 'codename')"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['auth.Group']", 'related_name': "'user_set'", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['auth.Permission']", 'related_name': "'user_set'", 'symmetrical': 'False'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'db_table': "'django_content_type'", 'object_name': 'ContentType', 'unique_together': "(('app_label', 'model'),)", 'ordering': "('name',)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'skills.skill': {
            'Meta': {'object_name': 'Skill'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'default': "'defaultimage'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'trainingbits': ('django.db.models.fields.related.ManyToManyField', [], {'null': 'True', 'blank': 'True', 'to': "orm['skills.TrainingBit']", 'symmetrical': 'False'}),
            'training_bits': ('django.db.models.fields.related.ManyToManyField', [], {'null': 'True', 'blank': 'True', 'to': "orm['skills.TrainingBit']", 'symmetrical': 'False'})
        },
        'skills.trainingbit': {
            'Meta': {'object_name': 'TrainingBit'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'default': "'defaultimage'"}),
            'is_draft': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'recommended': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['skills']
