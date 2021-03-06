# Generated by Django 2.1.1 on 2019-07-11 13:09

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('builder', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rear',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название')),
                ('image', models.ImageField(upload_to='', verbose_name='Изображение')),
                ('hex', models.CharField(help_text='Пример: #a4a4a4', max_length=7, verbose_name='Цвет')),
                ('order', models.PositiveSmallIntegerField(default=0)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='builder.Type')),
            ],
            options={
                'verbose_name': 'Тыл',
                'verbose_name_plural': 'Тылы',
                'ordering': ['order'],
            },
        ),
    ]
