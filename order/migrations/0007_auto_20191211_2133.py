# Generated by Django 2.1.1 on 2019-12-11 21:33

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_auto_20191015_0905'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='uuid',
            field=models.CharField(default=uuid.UUID('85967d9d-29f8-4a42-b99d-ab6f870144b8'), max_length=256, verbose_name='UUID'),
        ),
    ]