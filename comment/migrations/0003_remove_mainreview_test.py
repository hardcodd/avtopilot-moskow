# Generated by Django 2.1.1 on 2018-11-07 13:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0002_auto_20181107_1649'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mainreview',
            name='test',
        ),
    ]
