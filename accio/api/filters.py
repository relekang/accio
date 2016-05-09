from rest_framework import filters


class PermittedPermissionFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.permitted(request.user).distinct()
