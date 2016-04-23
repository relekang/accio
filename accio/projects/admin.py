from django.contrib import admin

from .models import Project, DeploymentTasks


class DeploymentTaskTabularInlineAdmin(admin.TabularInline):
    model = DeploymentTasks
    extra = 0


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'last_deploy']
    inlines = [DeploymentTaskTabularInlineAdmin]
