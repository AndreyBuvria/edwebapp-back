from django.contrib import admin

from .models import UserProfile

# Register your models here.

@admin.register(UserProfile)
class CustomUserAdmin(admin.ModelAdmin):
    #filter_horizontal = ('courses',)
    #list_display = ('username','first_name','last_name','email','about', 'role')
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.concrete_fields]