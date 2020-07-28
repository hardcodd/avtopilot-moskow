# Generated by Django 2.1.1 on 2020-03-10 09:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0007_auto_20200204_0301'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogWidget',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, verbose_name='Заголовок виджета')),
                ('image', models.ImageField(upload_to='', verbose_name='Изображение')),
                ('image_title', models.CharField(max_length=255, verbose_name='title')),
                ('url', models.URLField(help_text='URL will opened in new tab but URI in the same tab.', verbose_name='Ссылка')),
                ('order', models.PositiveIntegerField(blank=True, null=True)),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='settings.General')),
            ],
        ),
    ]