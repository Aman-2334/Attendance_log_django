import os
from attendance.models import AttendanceSession

class ErrorMessage():
    def __init__(self, message = "") -> None:
        self.error_message = message
    
    def get_error_response(self) -> map:
        if self.error_message:
            error_response = {"detail" : self.error_message}
        else:
            error_response = {}
        return error_response

def get_Attendance_Image_Directory(session: AttendanceSession) -> os.path:
    subject_code = session.subject.subject_code
    institution = session.subject.institution
    institution_id = f"{institution.name.replace(' ','_')}_{institution.id}"
    date = session.date.strftime("%d-%m-%Y")
    start_time = session.startTime.strftime("%H_%M")
    end_time = session.endTime.strftime("%H_%M")
    time_range = f"{start_time}-{end_time}"
    session_dir_path = os.path.join(
        "attendance\static\\attendance", institution_id, "session", subject_code, date, time_range)
    if not os.path.exists(session_dir_path):
        os.makedirs(session_dir_path)
    return session_dir_path