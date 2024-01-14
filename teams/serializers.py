from rest_framework import serializers

from teams.models import Team
from user.serializers import UserShowSerializer


class TeamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Team
        fields = ["id", "name", "members"]


class TeamDetailSerializer(TeamSerializer):
    members = UserShowSerializer(many=True, read_only=True)


class TeamListSerializer(TeamSerializer):
    members = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="email"
    )
