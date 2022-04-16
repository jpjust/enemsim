import pickletools
from django.db import models

# Timestamps
class TimeStampMixin(models.Model):
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

# Roles
class Role(TimeStampMixin):
    name            = models.CharField(max_length=10)
    description     = models.CharField(max_length=30)

    def __str__(self):
        return self.name

# Users
class User(TimeStampMixin):
    role            = models.ForeignKey(Role, on_delete=models.CASCADE)
    email           = models.CharField(max_length=100, unique=True)
    password        = models.CharField(max_length=100)
    fullname        = models.CharField(max_length=100)

    def __str__(self):
        return self.fullname

# Schools
class School(TimeStampMixin):
    name            = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Professors and teachers
class Professor(TimeStampMixin):
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    school          = models.ForeignKey(School, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.fullname

# Students
class Student(TimeStampMixin):
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    school          = models.ForeignKey(School, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.fullname

# Exams
class Exam(TimeStampMixin):
    student         = models.ForeignKey(Student, on_delete=models.CASCADE)
    score           = models.IntegerField

# Topics
class Topic(TimeStampMixin):
    text            = models.CharField(max_length=100)

    def __str__(self):
        return self.text

# Subjects
class Subject(TimeStampMixin):
    topic           = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text            = models.CharField(max_length=50)

    def __str__(self):
        return self.text

# Questions
class Question(TimeStampMixin):
    professor       = models.ForeignKey(Professor, on_delete=models.CASCADE)
    subject         = models.ForeignKey(Subject, on_delete=models.CASCADE)
    text            = models.CharField(max_length=1000)
    occurences      = models.IntegerField
    corrects        = models.IntegerField

    def __str__(self):
        return self.text

# Alternatives
class Alternative(TimeStampMixin):
    question        = models.ForeignKey(Question, on_delete=models.CASCADE)
    text            = models.CharField(max_length=200)
    correct         = models.BooleanField
    picks           = models.IntegerField

    def __str__(self):
        return self.text
