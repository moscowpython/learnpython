# Generated by Django 2.0.5 on 2018-06-10 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainpage', '0013_auto_20180610_1128'),
    ]

    operations = [
        migrations.AddField(
            model_name='graduatestories',
            name='story_section',
            field=models.TextField(choices=[('Есть опыт, хочу освоить новый язык', 'Есть опыт, хочу освоить новый язык'), ('Хочу новый навык или работу', 'Хочу новый навык или работу'), ('Никогда не программировал', 'Никогда не программировал')], default='Никогда не программировал', help_text='В какую из секций историй', verbose_name='Раздел истории'),
        ),
    ]
