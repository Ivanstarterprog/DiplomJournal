# Generated by Django 4.2.1 on 2023-06-11 06:04

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0011_alter_customuser_birthday_alter_customuser_role_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SemestrInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('course', models.PositiveIntegerField(db_index=True, default=1, verbose_name='Курс')),
                ('semestr', models.PositiveIntegerField(db_index=True, default=1, validators=[django.core.validators.MaxValueValidator(2), django.core.validators.MinValueValidator(1)], verbose_name='Семестр')),
                ('start_date', models.DateField(verbose_name='Дата начала семестра')),
                ('weeks', models.PositiveIntegerField(verbose_name='Количество недель')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Main.groups', verbose_name='Группа')),
            ],
            options={
                'verbose_name': 'Информация о семестрах',
                'verbose_name_plural': 'Информация о семестрах',
            },
        ),
    ]
