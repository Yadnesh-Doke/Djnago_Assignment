# Generated by Django 2.1.15 on 2020-07-02 13:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Covid_cases', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cases',
            old_name='newly_recovered',
            new_name='active_cases',
        ),
    ]
