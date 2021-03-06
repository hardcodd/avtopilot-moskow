# Generated by Django 2.1.1 on 2019-12-11 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0018_promocode'),
    ]

    operations = [
        migrations.AddField(
            model_name='universalcategory',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='Изображение (800x450)'),
        ),
        migrations.AddField(
            model_name='universalcategory',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, null=True, verbose_name='Слаг'),
        ),
    ]
