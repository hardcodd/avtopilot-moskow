# Generated by Django 2.1.1 on 2020-02-04 03:35

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0014_auto_20200204_0327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='uuid',
            field=models.CharField(default=uuid.UUID('c709708c-9acd-458f-9755-c1cf49340000'), max_length=256, verbose_name='UUID'),
        ),
    ]
