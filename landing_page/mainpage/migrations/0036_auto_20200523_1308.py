# Generated by Django 2.2.10 on 2020-05-23 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainpage', '0035_auto_20200320_0905'),
    ]

    operations = [
        migrations.AlterField(
            model_name='graduatestories',
            name='story_section',
            field=models.TextField(choices=[('Хочу новый навык или работу', 'Хочу новый навык или работу'), ('Есть опыт, хочу освоить новый язык', 'Есть опыт, хочу освоить новый язык'), ('Никогда не программировал', 'Никогда не программировал')], default='Никогда не программировал', help_text='В какую из секций историй', verbose_name='Раздел истории'),
        ),
    ]
