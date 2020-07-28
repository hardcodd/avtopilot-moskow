# Generated by Django 2.1.5 on 2020-04-14 13:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Footer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Footer', help_text='Только для администратора', max_length=255, verbose_name='Заголовок')),
                ('json', models.TextField(default='', verbose_name='JSON Контент')),
            ],
            options={
                'verbose_name': 'Footer',
                'verbose_name_plural': 'Footers',
            },
        ),
        migrations.CreateModel(
            name='Header',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Header', help_text='Только для администратора', max_length=255, verbose_name='Заголовок')),
                ('json', models.TextField(default='', verbose_name='JSON Контент')),
            ],
            options={
                'verbose_name': 'Header',
                'verbose_name_plural': 'Headers',
            },
        ),
        migrations.CreateModel(
            name='LandingPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Заголовок')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='Слаг')),
                ('theme_color', models.CharField(default='#7f00ff', max_length=255, verbose_name='Цвет браузера на мобилках')),
                ('show', models.BooleanField(default=True, verbose_name='Отображать кнопку "Наверх"')),
                ('background', models.CharField(default='linear-gradient(90deg, #7f00ff 0%, #00a3ff 100%)', max_length=255, verbose_name='Background')),
                ('color', models.CharField(default='#fff', max_length=255, verbose_name='Color')),
                ('bottom', models.PositiveSmallIntegerField(blank=True, default=10, null=True, verbose_name='Bottom Position')),
                ('right', models.PositiveSmallIntegerField(blank=True, default=10, null=True, verbose_name='Right Position')),
                ('left', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Left Position')),
                ('seo_title', models.CharField(blank=True, max_length=255, null=True, verbose_name='Сео заголовок')),
                ('keywords', models.CharField(blank=True, max_length=255, null=True, verbose_name='Кючевые слова')),
                ('meta_description', models.CharField(blank=True, max_length=255, null=True, verbose_name='Мета описание')),
                ('og_title', models.CharField(blank=True, max_length=255, null=True, verbose_name='Заголовок для соц. сетей')),
                ('og_description', models.CharField(blank=True, max_length=255, null=True, verbose_name='Описание для соц. сетей')),
                ('og_image', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Изображение для соц. сетей')),
            ],
            options={
                'verbose_name': 'Landing Page',
                'verbose_name_plural': 'Landing Pages',
            },
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Только для администратора', max_length=255, verbose_name='Заголовок')),
                ('order', models.PositiveIntegerField(db_index=True, default=0)),
                ('json', models.TextField(default='', verbose_name='JSON Контент')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sections', to='lp.LandingPage')),
            ],
            options={
                'verbose_name': 'Section',
                'verbose_name_plural': 'Sections',
                'ordering': ['order'],
            },
        ),
        migrations.AddField(
            model_name='header',
            name='parent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='headers', to='lp.LandingPage'),
        ),
        migrations.AddField(
            model_name='footer',
            name='parent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='footers', to='lp.LandingPage'),
        ),
    ]