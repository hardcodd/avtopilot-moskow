# Generated by Django 2.1.1 on 2020-02-04 03:01

import app.my_storage
import app.utils
from django.db import migrations
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0006_auto_20190220_1340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mainreview',
            name='image',
            field=easy_thumbnails.fields.ThumbnailerImageField(blank=True, null=True, storage=app.my_storage.MyStorage(), upload_to=app.utils.fn, verbose_name='Изображение'),
        ),
    ]