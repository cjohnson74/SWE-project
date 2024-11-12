# Generated by Django 4.2.9 on 2024-11-07 21:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("pages", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Assignments",
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
                ("canvas_id", models.CharField(max_length=255, unique=True)),
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True, null=True)),
                ("due_at", models.DateTimeField()),
                ("points_possible", models.IntegerField()),
                (
                    "submission_types",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "allowed_extensions",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("allowed_attempts", models.IntegerField()),
                (
                    "annotatable_attachment_id",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("anonymize_students", models.BooleanField()),
                ("anonymous_grading", models.BooleanField()),
                ("anonymous_instructor_annotations", models.BooleanField()),
                ("anonymous_peer_reviews", models.BooleanField()),
                ("anonymous_submissions", models.BooleanField()),
                (
                    "assignment_group_id",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("automatic_peer_reviews", models.BooleanField()),
                ("can_duplicate", models.BooleanField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "important_dates",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("in_closed_grading_period", models.BooleanField()),
                ("intra_group_peer_reviews", models.BooleanField()),
                ("is_quiz_assignment", models.BooleanField()),
                ("lock_at", models.DateTimeField()),
                ("lock_explanation", models.TextField(blank=True, null=True)),
                ("lock_info", models.TextField(blank=True, null=True)),
                ("locked_for_user", models.BooleanField()),
                (
                    "lti_context_id",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("max_name_length", models.IntegerField()),
                ("moderated_grading", models.BooleanField()),
                ("muted", models.BooleanField()),
                ("omit_from_final_grade", models.BooleanField()),
                ("only_visible_to_overrides", models.BooleanField()),
                (
                    "original_assignment_id",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "original_assignment_name",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "original_course_id",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "original_lti_resource_link_id",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "original_quiz_id",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("peer_reviews", models.BooleanField()),
                ("position", models.IntegerField()),
                ("post_manually", models.BooleanField()),
                ("post_to_sis", models.BooleanField()),
                ("published", models.BooleanField()),
                ("quiz_id", models.CharField(blank=True, max_length=255, null=True)),
                ("require_lockdown_browser", models.BooleanField()),
                ("restrict_quantitative_data", models.BooleanField()),
                (
                    "secure_params",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("submissions_download_url", models.URLField(blank=True, null=True)),
                ("unlock_at", models.DateTimeField()),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("visible_to_everyone", models.BooleanField()),
                ("workflow_state", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="Courses",
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
                ("course_id", models.CharField(max_length=255, unique=True)),
                ("account_id", models.CharField(max_length=255)),
                ("apply_assignment_group_weights", models.BooleanField()),
                ("blueprint", models.CharField(max_length=255)),
                ("calendar", models.CharField(max_length=255)),
                ("course_code", models.CharField(max_length=100)),
                ("course_color", models.CharField(max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("default_view", models.CharField(max_length=50)),
                ("end_at", models.DateTimeField()),
                ("enrollment_term_id", models.CharField(max_length=255)),
                ("enrollments", models.CharField(max_length=255)),
                ("friendly_name", models.CharField(max_length=255)),
                ("grade_passback_setting", models.CharField(max_length=255)),
                ("grading_standard_id", models.CharField(max_length=255)),
                ("hide_final_grades", models.BooleanField()),
                ("homeroom_course", models.BooleanField()),
                ("is_public", models.BooleanField()),
                ("is_public_to_auth_users", models.BooleanField()),
                ("license", models.CharField(max_length=255)),
                ("name", models.CharField(max_length=255)),
                ("public_syllabus", models.BooleanField()),
                ("public_syllabus_to_auth", models.BooleanField()),
                ("restrict_enrollments_to_course_dates", models.BooleanField()),
                ("root_account_id", models.CharField(max_length=255)),
                ("start_at", models.DateTimeField()),
                ("storage_quota_mb", models.IntegerField()),
                ("template", models.CharField(max_length=255)),
                ("time_zone", models.CharField(max_length=255)),
                ("uuid", models.CharField(max_length=255)),
                ("workflow_state", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="CustomTasks",
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
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True, null=True)),
                ("due_date", models.DateTimeField()),
                ("complete", models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name="Deadlines",
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
                ("canvas_id", models.CharField(max_length=255, unique=True)),
                ("title", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True, null=True)),
                ("deadline_date", models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name="Files",
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
                ("file_id", models.CharField(max_length=255, unique=True)),
                ("filename", models.CharField(max_length=255)),
                ("display_name", models.CharField(max_length=255)),
                ("url", models.URLField()),
                ("size", models.IntegerField()),
                ("content_type", models.CharField(max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="Quizzes",
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
                ("canvas_id", models.CharField(max_length=255, unique=True)),
                ("title", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True, null=True)),
                ("due_at", models.DateTimeField()),
                ("time_limit", models.IntegerField()),
                ("quiz_type", models.CharField(max_length=255)),
                ("allowed_attempts", models.IntegerField()),
                ("file_ids", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="quizzes",
                        to="pages.courses",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="StudentAssignments",
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
                ("completed", models.BooleanField()),
                (
                    "assignment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="student_assignments",
                        to="pages.assignments",
                    ),
                ),
                (
                    "custom_tasks",
                    models.ManyToManyField(
                        related_name="student_assignments", to="pages.customtasks"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Students",
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
                ("canvas_id", models.CharField(max_length=255, unique=True)),
                ("name", models.CharField(max_length=255)),
                ("sortable_name", models.CharField(max_length=255)),
                ("short_name", models.CharField(max_length=255)),
                ("login_id", models.CharField(max_length=255)),
                ("email", models.EmailField(max_length=254)),
                ("avatar_url", models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name="Submissions",
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
                ("canvas_id", models.CharField(max_length=255, unique=True)),
                ("submitted_at", models.DateTimeField()),
                ("score", models.FloatField()),
                (
                    "assignment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="submissions",
                        to="pages.assignments",
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="submissions",
                        to="pages.students",
                    ),
                ),
            ],
        ),
        migrations.RemoveField(
            model_name="assignment",
            name="course",
        ),
        migrations.DeleteModel(
            name="Deadline",
        ),
        migrations.DeleteModel(
            name="Exam",
        ),
        migrations.DeleteModel(
            name="File",
        ),
        migrations.RemoveField(
            model_name="quiz",
            name="course",
        ),
        migrations.RemoveField(
            model_name="studentassignment",
            name="assignment",
        ),
        migrations.RemoveField(
            model_name="studentassignment",
            name="custom_tasks",
        ),
        migrations.RemoveField(
            model_name="studentassignment",
            name="student",
        ),
        migrations.RemoveField(
            model_name="submission",
            name="assignment",
        ),
        migrations.RemoveField(
            model_name="submission",
            name="student",
        ),
        migrations.DeleteModel(
            name="Assignment",
        ),
        migrations.DeleteModel(
            name="Course",
        ),
        migrations.DeleteModel(
            name="CustomTask",
        ),
        migrations.DeleteModel(
            name="Quiz",
        ),
        migrations.DeleteModel(
            name="Student",
        ),
        migrations.DeleteModel(
            name="StudentAssignment",
        ),
        migrations.DeleteModel(
            name="Submission",
        ),
        migrations.AddField(
            model_name="studentassignments",
            name="student",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="student_assignments",
                to="pages.students",
            ),
        ),
        migrations.AddField(
            model_name="assignments",
            name="course",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="assignments",
                to="pages.courses",
            ),
        ),
    ]