# Generated by Django 4.2.7 on 2023-11-14 15:26

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx'),
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
