# Generated by Django 2.1.1 on 2020-02-04 03:06

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0010_auto_20200204_0304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='uuid',
            field=models.CharField(default=uuid.UUID('9676da8a-ebb5-47e8-8104-62fec7bd9309'), max_length=256, verbose_name='UUID'),
        ),
    ]
