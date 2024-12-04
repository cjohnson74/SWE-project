# Generated by Django 4.2.9 on 2024-11-23 05:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("pages", "0006_alter_assignmentbreakdown_focus_impprovement_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="AssignmentFile",
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
                ("file", models.FileField(upload_to="assignment_files/")),
                ("file_name", models.CharField(max_length=255)),
                ("file_type", models.CharField(max_length=100)),
                ("uploaded_at", models.DateTimeField(auto_now_add=True)),
                ("content", models.TextField(blank=True, null=True)),
                (
                    "assignment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="files",
                        to="pages.assignments",
                    ),
                ),
            ],
        ),
    ]
