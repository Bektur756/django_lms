# Generated by Django 3.2 on 2021-09-11 14:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='is_owner',
            new_name='is_student',
        ),
    ]
