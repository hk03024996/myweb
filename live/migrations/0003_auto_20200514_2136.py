# Generated by Django 2.1.8 on 2020-05-14 13:36

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('live', '0002_live_readed_num'),
    ]

    operations = [
        migrations.AlterField(
            model_name='live',
            name='content',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
