# Generated by Django 2.1.1 on 2019-08-03 15:49

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_auto_20190730_1431'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='uuid',
            field=models.CharField(default=uuid.UUID('cec0dbb9-2d61-4413-ad2b-dd7d270c1921'), max_length=256, verbose_name='UUID'),
        ),
    ]
