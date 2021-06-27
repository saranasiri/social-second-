from django.contrib import admin
from .models import post,comment,vote

admin.site.register(post)
admin.site.register(comment)
admin.site.register(vote)
