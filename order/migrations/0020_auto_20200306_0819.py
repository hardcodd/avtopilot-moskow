# Generated by Django 2.1.1 on 2020-03-06 08:19

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0019_auto_20200306_0809'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='uuid',
            field=models.CharField(default=uuid.UUID('fb8520a9-8072-4ce4-9174-a7e1e7b560b0'), max_length=256, verbose_name='UUID'),
        ),
    ]