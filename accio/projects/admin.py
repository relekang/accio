from django.contrib import admin
from django.template.defaultfilters import pluralize

from accio.projects import tasks
from .models import Project, DeploymentTask


class DeploymentTaskTabularInlineAdmin(admin.TabularInline):
    model = DeploymentTask
    extra = 0


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'last_deploy']
    inlines = [DeploymentTaskTabularInlineAdmin]
    actions = ['deploy_latest', 'update_webhook']

    def deploy_latest(self, request, queryset):
        for project in queryset:
            project.deploy_latest()

        self.message_user(
            request,
            '{0} project{1} was queued'.format(len(queryset), pluralize(len(queryset)))
        )

    deploy_latest.short_description = 'Deploy latest main branch'

    def update_webhook(self, request, queryset):
        for project in queryset:
            tasks.update_webhook.delay(project.pk)

        self.message_user(
            request,
            '{0} project{1} was queued'.format(len(queryset), pluralize(len(queryset)))
        )

    update_webhook.short_description = 'Update webhooks'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if not request.user.is_superuser:
            queryset = queryset.filter(owner__members=request.user)
        return queryset
