# Generated by Django 2.1.5 on 2019-05-07 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainpage', '0029_auto_20190507_2316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='graduatestories',
            name='story_section',
            field=models.TextField(choices=[('Есть опыт, хочу освоить новый язык', 'Есть опыт, хочу освоить новый язык'), ('Хочу новый навык или работу', 'Хочу новый навык или работу'), ('Никогда не программировал', 'Никогда не программировал')], default='Никогда не программировал', help_text='В какую из секций историй', verbose_name='Раздел истории'),
        ),
    ]
