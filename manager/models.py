from django.db import models


class Group(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=100)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    entry_guidance = models.TextField(max_length=10000)
    course_aims = models.TextField(max_length=10000)

    def __str__(self):
        return self.name
