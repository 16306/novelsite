# Generated by Django 2.0 on 2019-02-18 18:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0007_auto_20190218_2317'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['comment_time']},
        ),
    ]
