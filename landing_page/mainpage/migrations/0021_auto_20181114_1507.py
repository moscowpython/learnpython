# Generated by Django 2.0.5 on 2018-11-14 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainpage', '0020_learnpythoncourse_online_session_closed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='graduatestories',
            name='story_section',
            field=models.TextField(choices=[('Есть опыт, хочу освоить новый язык', 'Есть опыт, хочу освоить новый язык'), ('Никогда не программировал', 'Никогда не программировал'), ('Хочу новый навык или работу', 'Хочу новый навык или работу')], default='Никогда не программировал', help_text='В какую из секций историй', verbose_name='Раздел истории'),
        ),
    ]
