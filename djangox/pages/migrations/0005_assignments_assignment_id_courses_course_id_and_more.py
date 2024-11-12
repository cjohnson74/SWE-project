# Generated by Django 4.2.9 on 2024-11-12 13:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pages", "0004_remove_assignments_allowed_attempts_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="assignments",
            name="assignment_id",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="courses",
            name="course_id",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AlterField(
            model_name="assignments",
            name="updated_at",
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name="courses",
            name="created_at",
            field=models.DateTimeField(),
        ),
    ]
