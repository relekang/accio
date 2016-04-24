from django.contrib import admin
from django.template.defaultfilters import pluralize

from .models import Project, DeploymentTask


class DeploymentTaskTabularInlineAdmin(admin.TabularInline):
    model = DeploymentTask
    extra = 0


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'last_deploy']
    inlines = [DeploymentTaskTabularInlineAdmin]
    actions = ['deploy_latest']

    def deploy_latest(self, request, queryset):
        for project in queryset:
            project.deploy_latest()

        self.message_user(
            request,
            '{0} project{1} was queued'.format(len(queryset), pluralize(len(queryset)))
        )

    deploy_latest.short_description = 'Deploy latest main branch'
