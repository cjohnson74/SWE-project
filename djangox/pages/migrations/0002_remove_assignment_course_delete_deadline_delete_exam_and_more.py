# Generated by Django 4.2.9 on 2024-10-28 23:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assignment',
            name='course',
        ),
        migrations.DeleteModel(
            name='Deadline',
        ),
        migrations.DeleteModel(
            name='Exam',
        ),
        migrations.DeleteModel(
            name='File',
        ),
        migrations.RemoveField(
            model_name='quiz',
            name='course',
        ),
        migrations.RemoveField(
            model_name='studentassignment',
            name='assignment',
        ),
        migrations.RemoveField(
            model_name='studentassignment',
            name='custom_tasks',
        ),
        migrations.RemoveField(
            model_name='studentassignment',
            name='student',
        ),
        migrations.RemoveField(
            model_name='submission',
            name='assignment',
        ),
        migrations.RemoveField(
            model_name='submission',
            name='student',
        ),
        migrations.DeleteModel(
            name='Assignment',
        ),
        migrations.DeleteModel(
            name='Course',
        ),
        migrations.DeleteModel(
            name='CustomTask',
        ),
        migrations.DeleteModel(
            name='Quiz',
        ),
        migrations.DeleteModel(
            name='Student',
        ),
        migrations.DeleteModel(
            name='StudentAssignment',
        ),
        migrations.DeleteModel(
            name='Submission',
        ),
    ]