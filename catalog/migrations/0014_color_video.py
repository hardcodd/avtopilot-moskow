# Generated by Django 2.1.1 on 2019-04-29 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0013_auto_20190409_1714'),
    ]

    operations = [
        migrations.AddField(
            model_name='color',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to='', verbose_name='Видео превью'),
        ),
    ]
