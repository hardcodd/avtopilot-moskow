# Generated by Django 2.1.1 on 2020-06-17 14:39

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0024_auto_20200617_1438'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='uuid',
            field=models.CharField(default=uuid.UUID('eb9e79e5-e532-4185-a1ef-f9b93a9910a8'), max_length=256, verbose_name='UUID'),
        ),
    ]
