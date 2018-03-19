# Generated by Django 2.0.1 on 2018-03-19 23:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('beers', '0011_auto_20180318_1751'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecommendedBeer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('agreed', models.BooleanField(default=False)),
                ('beer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='beers.Beer')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
