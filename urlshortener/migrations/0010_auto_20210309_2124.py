# Generated by Django 3.1.7 on 2021-03-09 21:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('urlshortener', '0009_auto_20210309_2117'),
    ]

    operations = [
        migrations.CreateModel(
            name='UrlHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url_id', models.CharField(max_length=10)),
                ('ip_address', models.GenericIPAddressField()),
                ('date_time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AlterField(
            model_name='url',
            name='expires_after',
            field=models.DateField(default=datetime.datetime(2021, 3, 16, 21, 24, 55, 755515)),
        ),
    ]
