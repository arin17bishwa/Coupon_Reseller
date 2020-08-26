from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from .models import User, UserProfile


class AccountAdmin(UserAdmin):
    list_display = ('email','registration_no','date_joined','last_login','is_admin','is_staff')#What to display as columns
    search_fields = ('email','username','registration_no')#what to search by
    readonly_fields = ('last_login','date_joined','registration_no')#Non-editable fields

    filter_horizontal = ()#
    list_filter = ()#
    fieldsets = ()#NO IDEA WHAT IT DOES....JUST ADD FOR NOW(ERROR OTHERWISE)

class ProfileAdmin(admin.ModelAdmin):
    list_display = (
    'user','name', 'hall', 'veg','slug')  # What to display as columns
    search_fields = ('hall', 'name', 'veg')  # what to search by
    readonly_fields = ()  # Non-editable fields

    filter_horizontal = ()  #
    list_filter = ()  #
    fieldsets = ()  # NO IDEA WHAT IT DOES....JUST ADD FOR NOW(ERROR OTHERWISE)


admin.site.register(User,AccountAdmin)
admin.site.register(UserProfile,ProfileAdmin)