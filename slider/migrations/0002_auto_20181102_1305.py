# Generated by Django 2.1.1 on 2018-11-02 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slider', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slide',
            name='order',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
