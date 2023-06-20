# Generated by Django 4.2.1 on 2023-06-05 03:32

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0009_delete_semestrinfo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subject',
            name='type',
        ),
        migrations.AlterField(
            model_name='groups',
            name='start_year',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Год зачисления группы'),
        ),
        migrations.AlterField(
            model_name='speciality',
            name='code',
            field=models.CharField(db_index=True, max_length=8, verbose_name='Шифр специальности'),
        ),
        migrations.AlterField(
            model_name='speciality',
            name='name',
            field=models.CharField(db_index=True, max_length=70, verbose_name='Наименование специальности'),
        ),
        migrations.AlterField(
            model_name='speciality',
            name='shortName',
            field=models.CharField(default='', max_length=30, verbose_name='Сокращённое наименование специальности'),
        ),
        migrations.AlterField(
            model_name='studenttogroup',
            name='health',
            field=models.CharField(choices=[('MA', 'Основная'), ('SP', 'Специальная'), ('PO', 'Подготовительная')], default='MA', max_length=2, verbose_name='Группа здоровья'),
        ),
    ]