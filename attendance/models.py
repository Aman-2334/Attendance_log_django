from django.db import models
from institution.models import Subject
import json
import os


class AttendanceSession(models.Model):
    classCount = models.IntegerField(default=1)
    date = models.DateTimeField(
        auto_now=False, auto_created=False, auto_now_add=False)
    startTime = models.DateTimeField(
        auto_now=False, auto_now_add=False, auto_created=False)
    endTime = models.DateTimeField(
        auto_now=False, auto_now_add=False, auto_created=False)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    students = models.TextField()

    def set_students(self, students_list):
        self.students = json.dumps(students_list)

    def get_students(self):
        return json.loads(self.students)


def upload_to(instance, filename):
    from helper import get_Attendance_Image_Directory
    session_dir_path = get_Attendance_Image_Directory(
        instance.attendance_session)
    uploadPath = os.path.join(session_dir_path, filename)
    return uploadPath


class AttendanceImages(models.Model):
    image = models.ImageField(
        upload_to=upload_to, max_length=255)
    attendance_session = models.ForeignKey(
        AttendanceSession, on_delete=models.CASCADE, related_name='images')
