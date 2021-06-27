from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import profile,relation
class profileInline(admin.StackedInline):
    model = profile
    can_delete = False
class Extendedprofileadmin(UserAdmin):
    inlines = (profileInline,)

admin.site.unregister(User)
admin.site.register(User,Extendedprofileadmin)
admin.site.register(relation)