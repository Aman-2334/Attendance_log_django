from django.urls import path
from . import views

urlpatterns = [
    path('markOnlineAttendance',views.OnlineAttendanceView.as_view(), name='online-attendance')
]
