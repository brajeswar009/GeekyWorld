# Generated by Django 3.1.1 on 2020-09-19 11:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_blogcomment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogcomment',
            name='timestamp',
        ),
    ]
