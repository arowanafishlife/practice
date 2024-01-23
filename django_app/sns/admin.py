from django.contrib import admin
from .models import Message, Good, Following, Profile_text

# Register your models here.
admin.site.register(Message)
admin.site.register(Good)
admin.site.register(Following)
admin.site.register(Profile_text)