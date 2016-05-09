from rest_framework import permissions, viewsets

from accio.projects.models import Project
from accio.projects.serializers import ProjectSerializer
from ..filters import PermittedPermissionFilter


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = [PermittedPermissionFilter]
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]
