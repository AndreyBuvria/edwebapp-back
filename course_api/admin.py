from django.contrib import admin

from .models import CourseModel, TaskModel

# Register your models here.

admin.site.register([TaskModel,])
@admin.register(CourseModel)
class CustomUserAdmin(admin.ModelAdmin):
    filter_horizontal = ('members',)
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.concrete_fields]
