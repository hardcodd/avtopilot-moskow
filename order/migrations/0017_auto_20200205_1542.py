# Generated by Django 2.1.1 on 2020-02-05 15:42

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0016_auto_20200204_0343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='uuid',
            field=models.CharField(default=uuid.UUID('c53ff0bf-281f-4247-963b-ca3542c9b516'), max_length=256, verbose_name='UUID'),
        ),
    ]
