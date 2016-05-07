from rest_framework import serializers

from .models import Deployment, TaskResult


class TaskResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskResult
        fields = (
            'task_type',
            'order',
            'result',
            'started_at',
            'finished_at',
            'status',
        )


class DeploymentSerializer(serializers.ModelSerializer):
    task_results = TaskResultSerializer(many=True, read_only=True)

    class Meta:
        model = Deployment
        fields = (
            'id',
            'project',
            'ref',
            'short_ref',
            'started_at',
            'finished_at',
            'status',
            'task_results',
        )
