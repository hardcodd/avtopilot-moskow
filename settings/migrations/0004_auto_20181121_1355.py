# Generated by Django 2.1.1 on 2018-11-21 10:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0003_moderator'),
    ]

    operations = [
        migrations.CreateModel(
            name='Social',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('publish', models.BooleanField(default=True, verbose_name='Опубликовано')),
                ('link', models.URLField(verbose_name='Ссылка')),
                ('icon', models.CharField(help_text='<code><a href="https://fontawesome.com/icons?d=gallery&s=brands" target="blank">FontAwesome</a></code>', max_length=255, verbose_name='Иконка')),
                ('order', models.PositiveIntegerField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Соц.сеть',
                'verbose_name_plural': 'Соц.сети',
            },
        ),
        migrations.AddField(
            model_name='general',
            name='map',
            field=models.TextField(blank=True, null=True, verbose_name='Карта'),
        ),
        migrations.AddField(
            model_name='social',
            name='parent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='settings.General'),
        ),
    ]
