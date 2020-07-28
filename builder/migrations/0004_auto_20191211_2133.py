# Generated by Django 2.1.1 on 2019-12-11 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('builder', '0003_auto_20190803_1549'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='matebuilder',
            name='price',
        ),
        migrations.AlterField(
            model_name='matebuilder',
            name='set',
            field=models.TextField(blank=True, help_text='Каждый комплект с новой строки<br>Пример: <название>|<цена>', verbose_name='Комплекты'),
        ),
    ]