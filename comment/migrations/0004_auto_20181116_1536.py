# Generated by Django 2.1.1 on 2018-11-16 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0003_remove_mainreview_test'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]