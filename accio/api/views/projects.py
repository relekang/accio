from rest_framework import permissions, viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from accio.projects.models import Project
from accio.projects.serializers import ProjectSerializer

from ..filters import PermittedPermissionFilter


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = [PermittedPermissionFilter]
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]

    @detail_route(methods=['post'])
    def deploy(self, request, pk):
        project = self.get_object()
        project.deploy_latest()
        return Response({'status': 'pending'})
