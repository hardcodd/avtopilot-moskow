# Generated by Django 2.1.1 on 2019-07-30 14:31

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='uuid',
            field=models.CharField(default=uuid.UUID('c9c78cfd-32f5-4035-a9d8-6ce4458b89e2'), max_length=256, verbose_name='UUID'),
        ),
    ]