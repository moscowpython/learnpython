# Generated by Django 2.0.6 on 2018-06-09 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainpage', '0006_auto_20180609_1245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courators',
            name='curator_motto',
            field=models.CharField(help_text='Через тернии к звездам или что-нибудь такое', max_length=150, null=True, verbose_name='Девиз куратора'),
        ),
    ]
