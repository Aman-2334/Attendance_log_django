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
    subject_code = instance.attendance_session.subject.subject_code
    institution = instance.attendance_session.subject.institution
    institution_id = f"{institution.name.replace(' ','_')}_{institution.id}"
    date = instance.attendance_session.date.strftime("%d-%m-%Y")
    start_time = instance.attendance_session.startTime.strftime("%H_%M")
    end_time = instance.attendance_session.endTime.strftime("%H_%M")
    time_range = f"{start_time}-{end_time}"
    session_dir_path = os.path.join(
        "attendance\static\\attendance", institution_id, "session", subject_code, date, time_range)
    if not os.path.exists(session_dir_path):
        os.makedirs(session_dir_path)
    uploadPath = os.path.join(session_dir_path, filename)
    return uploadPath


class AttendanceImages(models.Model):
    image = models.ImageField(
        upload_to=upload_to, max_length=255)
    attendance_session = models.ForeignKey(
        AttendanceSession, on_delete=models.CASCADE, related_name='images')
