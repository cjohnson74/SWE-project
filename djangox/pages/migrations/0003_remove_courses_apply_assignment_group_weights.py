# Generated by Django 4.2.9 on 2024-11-12 12:22

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("pages", "0002_assignments_courses_customtasks_deadlines_files_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="courses",
            name="apply_assignment_group_weights",
        ),
    ]
