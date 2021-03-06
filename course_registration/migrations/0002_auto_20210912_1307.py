# Generated by Django 3.2 on 2021-09-12 13:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('course_registration', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseregistration',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='registered_subjects', to='courses.course'),
        ),
        migrations.AlterField(
            model_name='courseregistration',
            name='registration',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='subjects', to='course_registration.registration'),
        ),
        migrations.AlterField(
            model_name='courseregistration',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='registered_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='registration',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='registrations', to=settings.AUTH_USER_MODEL),
        ),
    ]
