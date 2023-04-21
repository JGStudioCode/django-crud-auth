from django.contrib import admin
# Mostrar la tabla en el ADMIN
from .models import Task

# Register your models here.

# Clase mostrar campos en el admin
class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ("created",)


# Registra vista SDMIN
admin.site.register(Task, TaskAdmin)
