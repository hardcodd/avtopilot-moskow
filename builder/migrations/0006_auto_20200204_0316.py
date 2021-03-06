# Generated by Django 2.1.1 on 2020-02-04 03:16

import app.my_storage
import app.utils
from django.db import migrations, models
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
        ('builder', '0005_auto_20200204_0301'),
    ]

    operations = [
        migrations.AddField(
            model_name='casebuilder',
            name='meta_description',
            field=models.CharField(blank=True, max_length=260, null=True, verbose_name='Мета описание'),
        ),
        migrations.AddField(
            model_name='casebuilder',
            name='meta_image',
            field=easy_thumbnails.fields.ThumbnailerImageField(blank=True, null=True, storage=app.my_storage.MyStorage(), upload_to=app.utils.fn, verbose_name='Изображение для соц. сетей'),
        ),
        migrations.AddField(
            model_name='casebuilder',
            name='meta_keywords',
            field=models.CharField(blank=True, max_length=160, null=True, verbose_name='Ключевые слова'),
        ),
        migrations.AddField(
            model_name='casebuilder',
            name='seo_title',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='СЕО Заголовок'),
        ),
    ]
