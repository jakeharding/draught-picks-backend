# Generated by Django 2.0.1 on 2018-03-11 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beers', '0003_auto_20180204_2209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beer',
            name='ibu',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True),
        ),
    ]
