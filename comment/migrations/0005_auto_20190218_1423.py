# Generated by Django 2.1.1 on 2019-02-18 14:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0004_auto_20181116_1536'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='publish_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 2, 18, 14, 23, 4, 304532), null=True),
        ),
    ]
