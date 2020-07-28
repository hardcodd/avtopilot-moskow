# Generated by Django 2.1.1 on 2018-11-07 12:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0002_general_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='Moderator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Имя')),
                ('email', models.EmailField(max_length=254)),
                ('active', models.BooleanField(default=True, verbose_name='Активный')),
                ('order', models.PositiveIntegerField(blank=True, null=True)),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='settings.General')),
            ],
        ),
    ]
