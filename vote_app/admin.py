from django.contrib import admin
from vote_app.models import Profile, Posts, Customuser, Comments
# Register your models here.

admin.site.register(Profile)
admin.site.register(Posts)
admin.site.register(Customuser)
admin.site.register(Comments)