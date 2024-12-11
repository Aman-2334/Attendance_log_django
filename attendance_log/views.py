# from django.contrib.auth import get_user_model
# from django.http import HttpResponseForbidden
# from django_eventstream import get_event_stream_view
# from rest_framework_simplejwt.authentication import JWTAuthentication
# from rest_framework.exceptions import AuthenticationFailed

# def custom_event_stream_view(request, username, **kwargs):
#     jwt_authenticator = JWTAuthentication()
#     try:
#         user, token = jwt_authenticator.authenticate(request)
#         if user is None or user.username != username:
#             return HttpResponseForbidden("Unauthorized access")
#         request.user = user
#     except AuthenticationFailed:
#         return HttpResponseForbidden("Invalid token")

#     try:
#         user = get_user_model().objects.get(username=username)
#         request.user = user
#     except get_user_model().DoesNotExist:
#         return HttpResponseForbidden("User not found")

#     event_stream_view = get_event_stream_view(kwargs.get('format_channels', []))
#     return event_stream_view(request, username=username, **kwargs)
