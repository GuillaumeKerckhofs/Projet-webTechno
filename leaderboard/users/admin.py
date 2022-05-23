from django.contrib import admin
from .models import CustomUser,Team,Membership
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea


class UserAdminConfig(UserAdmin):
    model = CustomUser

    ordering = ('user_name',)
    search_fields = ('user_name', 'email', 'first_name','last_name',)
    list_filter = ('user_name', 'email', 'first_name', 'last_name','is_dev', 'is_active', 'is_staff')
    list_display = ('user_name', 'email', 'first_name', 'last_name', 'is_dev',
                    'is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('user_name', 'email', 'first_name','last_name',)}),
        ('Permissions', {'fields': ('is_staff',)}),
        ('Personal', {'fields': ('is_dev',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user_name', 'email', 'first_name', 'last_name', 'password1', 'password2', 'is_staff','is_dev')}
         ),
    )

class MyAdminView(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        super(MyAdminView, self).save_model(request, obj, form, change)

admin.site.register(CustomUser, UserAdminConfig)
admin.site.register(Team)
admin.site.register(Membership)