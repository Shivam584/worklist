# Generated by Django 3.2.5 on 2022-06-28 04:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('baseapp', '0005_table_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='table',
            name='user',
        ),
    ]
