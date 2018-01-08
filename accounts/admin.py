from django.contrib import admin
from accounts.models import UserType
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# Register your models here.
class ProfileInline(admin.StackedInline):
    model = UserType
    


class IspUserAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'is_staff', 'is_superuser', 'is_active','usertype')
    list_filter = ('usertype__type','is_active','date_joined', 'last_login', 'is_staff', 'is_superuser', )
    inlines = (ProfileInline,)
    
    actions= ['activate_user', 'deactivate_user']
    
    def activate_user(self, request, queryset):
        queryset.update(is_active=True)
    activate_user.short_description = "Activate Users"
    
    def deactivate_user(self, request, queryset):
        queryset.update(is_active=False)
    deactivate_user.short_description = "Deactivate Users"

admin.site.unregister(User)
admin.site.register(User, IspUserAdmin)