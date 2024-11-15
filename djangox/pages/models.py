from django.db import models

class fileModel(models.Model):
    file = models.FileField(upload_to='uploads/')
    # or for images specifically
    # image = models.ImageField(upload_to='images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    def delete(self, *args, **kwargs):
        # Delete the file from the file system
        self.file.delete(save=False)
        # Delete the model instance
        super().delete(*args, **kwargs)

class Students(models.Model):
    canvas_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    sortable_name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=255)
    login_id = models.CharField(max_length=255)
    email = models.EmailField()
    avatar_url = models.URLField()

    def __str__(self):
        return self.name
    
class Courses(models.Model):
    course_id = models.CharField(max_length=255, default=1)
    created_at = models.DateTimeField()
    course_code = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    workflow_state = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class Assignments(models.Model):
    assignment_id = models.CharField(max_length=255, default=1)
    canvas_id = models.CharField(max_length=255, unique=True)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, related_name='assignments', default=1)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    due_at = models.DateTimeField(blank=True, null=True)
    points_possible = models.IntegerField(blank=True, null=True)
    submission_types = models.CharField(max_length=255, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name

class AssignmentBreakdown(models.Model):
    assignment = models.ForeignKey(Assignments, on_delete=models.CASCADE, related_name='assignment_breakdown')
    total_estimated_time = models.CharField(max_length=255)
    work_distribution = models.TextField()
    breaks_and_buffer = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.assignment.name} - Breakdown"

class AssignmentBreakdownTask(models.Model):
    breakdown = models.ForeignKey(AssignmentBreakdown, on_delete=models.CASCADE, related_name='tasks')
    task_number = models.IntegerField()
    description = models.TextField()
    estimated_time = models.CharField(max_length=255)
    due_date = models.DateTimeField()
    completed = models.BooleanField(default=False)
    tips = models.TextField(blank=True, null=True)
    priority = models.CharField(max_length=50)
    distraction_mitigation = models.TextField(blank=True, null=True)
    focus_techniques = models.TextField(blank=True, null=True)
    reward = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.breakdown.assignment.name} - Task {self.task_number}"

class YouTubeResource(models.Model):
    task = models.ForeignKey(AssignmentBreakdownTask, on_delete=models.CASCADE, related_name='youtube_resources')
    title = models.CharField(max_length=255)
    link = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.task.breakdown.assignment.name} - {self.title}"

class StudentAssignments(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE, related_name='student_assignments')
    assignment = models.ForeignKey(Assignments, on_delete=models.CASCADE, related_name='student_assignments')
    completed = models.BooleanField()
    breakdown = models.ManyToManyField(AssignmentBreakdown, related_name='student_assignments')

    def __str__(self):
        return f"{self.student.name} - {self.assignment.name}"
    
class Quizzes(models.Model):
    canvas_id = models.CharField(max_length=255, unique=True)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, related_name='quizzes')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    due_at = models.DateTimeField()
    time_limit = models.IntegerField()
    quiz_type = models.CharField(max_length=255)
    allowed_attempts = models.IntegerField()
    file_ids = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title

class Submissions(models.Model):
    canvas_id = models.CharField(max_length=255, unique=True)
    assignment = models.ForeignKey(Assignments, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(Students, on_delete=models.CASCADE, related_name='submissions')
    submitted_at = models.DateTimeField()
    score = models.FloatField()

    def __str__(self):
        return f"{self.student.name} - {self.assignment.name}"

class Files(models.Model):
    file_id = models.CharField(max_length=255, unique=True)
    filename = models.CharField(max_length=255)
    display_name = models.CharField(max_length=255)
    url = models.URLField()
    size = models.IntegerField()
    content_type = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.filename

class Deadlines(models.Model):
    canvas_id = models.CharField(max_length=255, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    deadline_date = models.DateTimeField()

    def __str__(self):
        return self.title
