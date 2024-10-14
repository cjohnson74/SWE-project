# Generated by Django 5.1.2 on 2024-10-12 16:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Course",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("canvas_id", models.CharField(max_length=100, unique=True)),
                ("name", models.CharField(max_length=200)),
                ("course_code", models.CharField(max_length=20)),
                ("start_at", models.DateTimeField()),
                ("end_at", models.DateTimeField()),
                ("public_description", models.TextField()),
                ("term_id", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="CustomTask",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200)),
                ("description", models.TextField()),
                ("due_date", models.DateTimeField()),
                ("complete", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="Deadline",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("canvas_id", models.CharField(max_length=100, unique=True)),
                ("title", models.CharField(max_length=200)),
                ("description", models.TextField()),
                ("deadline_date", models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name="Exam",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("canvas_id", models.CharField(max_length=100, unique=True)),
                ("title", models.CharField(max_length=200)),
                ("description", models.TextField()),
                ("exam_date", models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name="File",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("canvas_id", models.CharField(max_length=100, unique=True)),
                ("filename", models.CharField(max_length=200)),
                ("content_type", models.CharField(max_length=100)),
                ("url", models.URLField()),
                ("size", models.IntegerField()),
                ("created_at", models.DateTimeField()),
                ("updated_at", models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name="Student",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("canvas_id", models.CharField(max_length=100, unique=True)),
                ("name", models.CharField(max_length=200)),
                ("sortable_name", models.CharField(max_length=200)),
                ("short_name", models.CharField(max_length=100)),
                ("login_id", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=254)),
                ("avatar_url", models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name="Assignment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("canvas_id", models.CharField(max_length=100, unique=True)),
                ("name", models.CharField(max_length=200)),
                ("description", models.TextField()),
                ("due_at", models.DateTimeField()),
                ("points_possible", models.IntegerField()),
                ("submission_types", models.JSONField()),
                ("allowed_extensions", models.JSONField()),
                ("file_ids", models.JSONField()),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="pages.course"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Quiz",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("canvas_id", models.CharField(max_length=100, unique=True)),
                ("title", models.CharField(max_length=200)),
                ("description", models.TextField()),
                ("due_at", models.DateTimeField()),
                ("time_limit", models.IntegerField()),
                ("quiz_type", models.CharField(max_length=50)),
                ("allowed_attempts", models.IntegerField()),
                ("file_ids", models.JSONField()),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="pages.course"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="StudentAssignment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("completed", models.BooleanField(default=False)),
                (
                    "assignment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="pages.assignment",
                    ),
                ),
                (
                    "custom_tasks",
                    models.ManyToManyField(blank=True, to="pages.customtask"),
                ),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="pages.student"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Submission",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("canvas_id", models.CharField(max_length=100, unique=True)),
                ("submitted_at", models.DateTimeField()),
                ("score", models.IntegerField()),
                (
                    "assignment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="pages.assignment",
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="pages.student"
                    ),
                ),
            ],
        ),
    ]
