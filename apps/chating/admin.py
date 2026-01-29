from mailbox import Message
from django.contrib import admin
from unfold.admin import ModelAdmin
from apps.chating.models import Message

# Register your models here.
@admin.register(Message)
class MessageAdmin(ModelAdmin):
    list_display = ('sender', 'receiver', 'text', 'timestamp', 'is_read')
    search_fields = ('sender__email', 'receiver__email', 'text')
    list_filter = ('is_read', 'timestamp')

    fieldsets = (
        ('Message Info', {'fields': ('sender', 'receiver', 'text', 'is_read')}),
    )