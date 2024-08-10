from django.contrib import admin
from .models import Role, User, User_Role, User_Institute
# Register your models here.
admin.site.register(Role)
admin.site.register(User)
admin.site.register(User_Role)
admin.site.register(User_Institute)
