# Generated by Django 2.1.1 on 2018-10-18 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='General',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, verbose_name='Заголовок сайта')),
                ('title_part', models.CharField(blank=True, max_length=255, verbose_name='Вторая часть заголовка')),
                ('divider', models.CharField(blank=True, max_length=3, verbose_name='Разделитель заголовка')),
                ('keywords', models.CharField(blank=True, max_length=255, verbose_name='Ключевые слова')),
                ('description', models.CharField(blank=True, max_length=255, verbose_name='Описание')),
                ('meta_image', models.ImageField(blank=True, upload_to='', verbose_name='Изображение для соц.сетей')),
                ('phone_free', models.CharField(blank=True, max_length=255, verbose_name='Телефон бесплатной линии')),
                ('phone', models.CharField(blank=True, max_length=255, verbose_name='Телефон')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='E-mail')),
                ('city', models.CharField(blank=True, max_length=255, verbose_name='Город')),
                ('address', models.CharField(blank=True, max_length=255, verbose_name='Адрес')),
                ('zip', models.CharField(blank=True, max_length=255, verbose_name='Индекс')),
                ('work_time', models.CharField(blank=True, max_length=255, verbose_name='Время работы')),
            ],
            options={
                'verbose_name': 'Опции сайта',
                'verbose_name_plural': 'Опции сайта',
            },
        ),
    ]
