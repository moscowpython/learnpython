# Generated by Django 2.0.6 on 2018-06-09 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainpage', '0011_auto_20180609_1416'),
    ]

    operations = [
        migrations.AddField(
            model_name='learnpythoncourseprices',
            name='price_range_start_date',
            field=models.DateField(blank=True, help_text='Когда начинается данное предложение', null=True, verbose_name='Дата начала интервала'),
        ),
        migrations.AlterField(
            model_name='learnpythoncourseprices',
            name='price_range_end_date',
            field=models.DateField(blank=True, help_text='Когда истекает данное предложение', null=True, verbose_name='Дата окончания интервала'),
        ),
    ]
