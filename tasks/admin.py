from django.contrib import admin

# Register your models here.

from .models import User,Todo,SubTask

class TodoAdmin(admin.ModelAdmin):
    #readonly_fields=("slug",)
   prepopulated_fields={"slug":("task_desc",)}
   list_filter=("tag","status")
   list_display=("task_desc","task_deadline")


admin.site.register(User)
admin.site.register(Todo,TodoAdmin)
admin.site.register(SubTask)