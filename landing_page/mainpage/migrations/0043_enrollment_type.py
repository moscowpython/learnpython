# Generated by Django 4.2.4 on 2023-09-08 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainpage', '0042_enrollment_platim_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='enrollment',
            name='type',
            field=models.CharField(blank=True, choices=[('BASE', 'BASE'), ('ADVANCED', 'ADVANCED')], max_length=10, null=True),
        ),
    ]
