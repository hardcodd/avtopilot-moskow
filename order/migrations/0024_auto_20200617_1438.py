# Generated by Django 2.1.1 on 2020-06-17 14:38

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0023_auto_20200608_1318'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='uuid',
            field=models.CharField(default=uuid.UUID('9072354d-84a5-4558-912b-82236a22ca6a'), max_length=256, verbose_name='UUID'),
        ),
    ]