# Generated by Django 2.1.1 on 2020-06-08 13:18

from django.db import migrations, models
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0027_auto_20200310_0911'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviews',
            name='meta_description',
            field=models.CharField(blank=True, max_length=260, null=True, verbose_name='Мета описание'),
        ),
        migrations.AddField(
            model_name='reviews',
            name='meta_image',
            field=easy_thumbnails.fields.ThumbnailerImageField(blank=True, null=True, upload_to='', verbose_name='Изображение для соц. сетей'),
        ),
        migrations.AddField(
            model_name='reviews',
            name='meta_keywords',
            field=models.CharField(blank=True, max_length=160, null=True, verbose_name='Ключевые слова'),
        ),
        migrations.AddField(
            model_name='reviews',
            name='seo_title',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='СЕО Заголовок'),
        ),
    ]
