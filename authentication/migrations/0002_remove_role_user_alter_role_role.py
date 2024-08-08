# Generated by Django 5.0.8 on 2024-08-08 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='role',
            name='user',
        ),
        migrations.AlterField(
            model_name='role',
            name='role',
            field=models.CharField(choices=[('ADMIN', 'Admin'), ('TEACHER', 'Teacher'), ('STUDENT', 'Student')], max_length=255),
        ),
    ]
