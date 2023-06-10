from django.contrib import admin

from .models import Subscribe, User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'role',
        'is_superuser'
    )
    list_filter = ('role', 'is_superuser')
    list_editable = ('role',)
    search_fields = ('username',)


admin.site.register(User, UserAdmin)


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('user', 'author',)
