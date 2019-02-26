from django.contrib import admin
from .models import Profile, Collection

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


class CollectionInline(admin.StackedInline):
    model = Collection
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, CollectionInline)
    list_display = ('username', 'nikename', 'email', 'is_staff', 'is_active', 'is_superuser')

    def nikename(self, obj):
        return obj.profile.nikename
    nikename.short_description = '昵称'


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'nikename')


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('collection',)
