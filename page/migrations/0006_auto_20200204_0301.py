# Generated by Django 2.1.1 on 2020-02-04 03:01

import app.my_storage
import app.utils
from django.db import migrations
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0005_remove_info_script'),
    ]

    operations = [
        migrations.AlterField(
            model_name='about',
            name='meta_image',
            field=easy_thumbnails.fields.ThumbnailerImageField(blank=True, null=True, upload_to='', verbose_name='Изображение для соц. сетей'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='meta_image',
            field=easy_thumbnails.fields.ThumbnailerImageField(blank=True, null=True, upload_to='', verbose_name='Изображение для соц. сетей'),
        ),
        migrations.AlterField(
            model_name='help',
            name='meta_image',
            field=easy_thumbnails.fields.ThumbnailerImageField(blank=True, null=True, upload_to='', verbose_name='Изображение для соц. сетей'),
        ),
        migrations.AlterField(
            model_name='info',
            name='meta_image',
            field=easy_thumbnails.fields.ThumbnailerImageField(blank=True, null=True, upload_to='', verbose_name='Изображение для соц. сетей'),
        ),
        migrations.AlterField(
            model_name='ouroffer',
            name='image',
            field=easy_thumbnails.fields.ThumbnailerImageField(blank=True, null=True, upload_to='', verbose_name='Фото (510x287)'),
        ),
        migrations.AlterField(
            model_name='portfolio',
            name='meta_image',
            field=easy_thumbnails.fields.ThumbnailerImageField(blank=True, null=True, upload_to='', verbose_name='Изображение для соц. сетей'),
        ),
        migrations.AlterField(
            model_name='staffmember',
            name='image',
            field=easy_thumbnails.fields.ThumbnailerImageField(blank=True, null=True, upload_to='', verbose_name='Фото (510x595)'),
        ),
        migrations.AlterField(
            model_name='staffmember',
            name='meta_image',
            field=easy_thumbnails.fields.ThumbnailerImageField(blank=True, null=True, upload_to='', verbose_name='Изображение для соц. сетей'),
        ),
        migrations.AlterField(
            model_name='work',
            name='image',
            field=easy_thumbnails.fields.ThumbnailerImageField(blank=True, null=True, storage=app.my_storage.MyStorage(), upload_to=app.utils.fn, verbose_name='Изображение (800x450)'),
        ),
    ]
