from django.contrib import admin

from .models import Deployment, TaskResult


class DeploymentTaskStackedInline(admin.StackedInline):
    model = TaskResult
    extra = 0
    exclude = ['result']
    readonly_fields = [
        'task_type',
        'order',
        'config',
        'deployment',
        'display_result',
        'started_at',
        'finished_at',
        'status',
    ]


@admin.register(Deployment)
class DeploymentAdmin(admin.ModelAdmin):
    list_display = ['project', 'ref', 'status', 'started_at', 'finished_at']
    inlines = [DeploymentTaskStackedInline]
    readonly_fields = ['project', 'status', 'ref', 'started_at', 'finished_at']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if not request.user.is_superuser:
            queryset = queryset.filter(project__owner__members=request.user)
        return queryset
