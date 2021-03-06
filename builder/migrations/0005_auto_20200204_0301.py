# Generated by Django 2.1.1 on 2020-02-04 03:01

from django.db import migrations
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
        ('builder', '0004_auto_20191211_2133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='base',
            name='image',
            field=easy_thumbnails.fields.ThumbnailerImageField(upload_to='', verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='color',
            name='image',
            field=easy_thumbnails.fields.ThumbnailerImageField(upload_to='', verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='matebuilder',
            name='bearing',
            field=easy_thumbnails.fields.ThumbnailerImageField(blank=True, upload_to='', verbose_name='Изображение подпятника'),
        ),
        migrations.AlterField(
            model_name='matebuilder',
            name='nameplate_image',
            field=easy_thumbnails.fields.ThumbnailerImageField(blank=True, upload_to='', verbose_name='Изображение шильдика'),
        ),
        migrations.AlterField(
            model_name='matecolor',
            name='image',
            field=easy_thumbnails.fields.ThumbnailerImageField(upload_to='', verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='rear',
            name='image',
            field=easy_thumbnails.fields.ThumbnailerImageField(upload_to='', verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='seamcolor',
            name='image',
            field=easy_thumbnails.fields.ThumbnailerImageField(upload_to='', verbose_name='Изображение'),
        ),
    ]
