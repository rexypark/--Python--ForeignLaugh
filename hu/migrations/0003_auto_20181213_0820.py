# Generated by Django 2.1.3 on 2018-12-13 08:20

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('hu', '0002_delete_addpost'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2018, 12, 13, 8, 20, 13, 816069, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='post',
            name='homePage',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
