# Generated by Django 5.0.8 on 2024-11-17 20:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institution', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject_name', models.CharField(max_length=512)),
                ('subject_code', models.CharField(max_length=512)),
                ('insititution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subject_in_institution', to='institution.institution')),
                ('instructor', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='subject_instructor', to=settings.AUTH_USER_MODEL)),
                ('student', models.ManyToManyField(related_name='student_in_subject', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddConstraint(
            model_name='subject',
            constraint=models.UniqueConstraint(fields=('subject_code', 'insititution'), name='unique_subject_in_institution'),
        ),
    ]
