from rest_framework import serializers

from ..deployments.serializers import DeploymentSerializer
from ..organizations.serializers import OrganizationSerializer
from .models import Project


class ProjectSerializer(serializers.ModelSerializer):
    owner = OrganizationSerializer()
    last_deploy = DeploymentSerializer(read_only=True)

    class Meta:
        model = Project
        fields = (
            'id',
            'owner',
            'name',
            'vcs_url',
            'deploy_on',
            'last_deploy',
        )
