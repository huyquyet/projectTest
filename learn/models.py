from django.contrib.auth.models import User
from django.db import models
from django.conf import settings


# Create your models here.
from django.utils import timezone


class Subject(models.Model):
    name = models.TextField()
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    begin_at = models.DateTimeField()
    end_at = models.DateTimeField()
    status = models.BooleanField(default=False, help_text="Activity")
    users = models.ManyToManyField(User, through='UserSubject', related_name='subjects')

    def check_time_end_subject(self, time):
        if time > self.end_at:
            return False
        else:
            return True

    # def __str__(self):
    #     return self.name

    def __unicode__(self):
        return self.name

    def joined_user(self, user, status=None):
        if status is None:
            if UserSubject.objects.filter(user_id=user, subject_id=self).exists():
                return True
            else:
                return False
        else:
            if UserSubject.objects.filter(user_id=user, subject_id=self, status=status).exists():
                return True
            else:
                return False


class Course(models.Model):
    name = models.TextField()
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    begin_at = models.DateTimeField()
    end_at = models.DateTimeField()
    subjects = models.ManyToManyField(Subject, related_name='courses')
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, through="UserCourse", related_name="courses")

    # def __str__(self):
    #     return self.name
    def __unicode__(self):
        return self.name


class Task(models.Model):
    name = models.TextField()
    subject_id = models.ForeignKey(Subject, related_name='task')
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    begin_at = models.DateTimeField()
    end_at = models.DateTimeField()
    users = models.ManyToManyField(User, through='UserTask', related_name='tasks')

    def __str__(self):
        return self.name

    def joined_user_task(self, user, status=None):
        # Search user is exist in UserTask
        if status is None:
            if UserTask.objects.filter(user_id=user, task_id=self).exists():
                return True
            else:
                return False
        # Search user status in UserTask
        else:
            if UserTask.objects.filter(user_id=user, task_id=self, status=status).exists():
                return True
            else:

                return False


class UserCourse(models.Model):
    user_id = models.ForeignKey(User)
    course_id = models.ForeignKey(Course)
    status = models.BooleanField(default=True)


class UserSubject(models.Model):
    user_id = models.ForeignKey(User)
    subject_id = models.ForeignKey(Subject)
    status = models.BooleanField(default=True)


class UserTask(models.Model):
    user_id = models.ForeignKey(User)
    task_id = models.ForeignKey(Task)
    status = models.BooleanField(default=True)
