# Generated by Django 2.0.5 on 2018-05-26 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainpage', '0005_learnpythoncourse'),
    ]

    operations = [
        migrations.CreateModel(
            name='Courators',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('curator_name', models.CharField(max_length=50, verbose_name='Имя и фамилия куратора')),
                ('curator_bio', models.TextField(verbose_name='Биография куратора')),
                ('curator_motto', models.CharField(max_length=150, verbose_name='Девиз куратора')),
                ('curator_photo', models.ImageField(upload_to='')),
            ],
            options={
                'verbose_name_plural': 'LearnPython Кураторы',
            },
        ),
        migrations.AlterModelOptions(
            name='moscowpythonmeetup',
            options={'verbose_name_plural': 'MoscowPython Митапы'},
        ),
    ]
