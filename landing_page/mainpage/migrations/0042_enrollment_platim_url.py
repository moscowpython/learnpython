# Generated by Django 4.2.4 on 2023-08-25 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainpage', '0041_enrollment'),
    ]

    operations = [
        migrations.AddField(
            model_name='enrollment',
            name='platim_url',
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
    ]
