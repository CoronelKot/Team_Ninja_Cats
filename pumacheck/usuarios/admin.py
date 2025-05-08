from django.contrib.admin.models import LogEntry
from django.contrib import admin
from usuarios.models import Usuario

LogEntry.user.field.remote_field.model = Usuario 
admin.site.register(Usuario)

@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['action_time', 'user', 'content_type', 'object_repr', 'action_flag']
    readonly_fields = [f.name for f in LogEntry._meta.fields]
