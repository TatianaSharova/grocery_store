from django.contrib import admin

from .models import User
from store.constans import EMPTY_VALUE


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username',
                    'email', 'date_joined')
    list_filter = ('username', 'email',)
    search_fields = ('email', 'username')
    empty_value_display = EMPTY_VALUE
