# Generated by Django 2.0.1 on 2018-03-18 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20180313_2244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='draughtpicksuser',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
