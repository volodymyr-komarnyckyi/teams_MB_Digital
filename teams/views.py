from rest_framework import viewsets

from teams.models import Team
from teams.serializers import (
    TeamSerializer,
    TeamDetailSerializer,
    TeamListSerializer
)


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    def get_queryset(self):
        queryset = self.queryset

        if self.action in ("list", "retrieve"):
            queryset = queryset.prefetch_related("members")

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return TeamListSerializer

        if self.action == "retrieve":
            return TeamDetailSerializer

        return TeamSerializer
