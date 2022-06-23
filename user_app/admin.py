from django.contrib import admin
from .models import Profile, Skill, Message, Chat 
# Register your models here.
admin.site.register(Profile)
admin.site.register(Skill)
admin.site.register(Message)
admin.site.register(Chat)