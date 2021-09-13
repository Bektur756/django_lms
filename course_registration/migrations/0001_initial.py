# Generated by Django 3.2 on 2021-09-12 12:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('courses', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseRegistration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveSmallIntegerField(default=1)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='reserve_items', to='courses.course')),
            ],
            options={
                'db_table': 'course_registration',
            },
        ),
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_credits', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('required', 'обязательный'), ('prerequisite', 'требуется пререквизиты'), ('free', 'свободный')], default='free', max_length=20)),
                ('courses', models.ManyToManyField(through='course_registration.CourseRegistration', to='courses.Course')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='registration', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'registration',
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddField(
            model_name='courseregistration',
            name='registration',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='items', to='course_registration.registration'),
        ),
        migrations.AddField(
            model_name='courseregistration',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='reserve_items', to=settings.AUTH_USER_MODEL),
        ),
    ]