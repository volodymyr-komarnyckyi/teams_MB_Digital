from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from teams.models import Team
from user.models import User
from teams.serializers import TeamSerializer, TeamDetailSerializer, TeamListSerializer


class TeamSerializerTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(email="user1@example.com", first_name="John", last_name="Doe")
        self.team_data = {
            "name": "Team A",
            "members": [self.user1.id],
        }

    def test_team_serializer(self):
        serializer = TeamSerializer(data=self.team_data)
        if not serializer.is_valid():
            print(serializer.errors)
        self.assertTrue(serializer.is_valid())

    def test_team_detail_serializer(self):
        team = Team.objects.create(name="Team A")
        team.members.add(self.user1)
        serializer = TeamDetailSerializer(instance=team)
        self.assertIn("members", serializer.data)
        self.assertIsInstance(serializer.data["members"], list)
        self.assertEqual(serializer.data["members"][0]["email"], self.user1.email)

    def test_team_list_serializer(self):
        team = Team.objects.create(name="Team A")
        team.members.add(self.user1)
        serializer = TeamListSerializer(instance=team)
        self.assertIn("members", serializer.data)
        self.assertIsInstance(serializer.data["members"], list)
        self.assertEqual(serializer.data["members"][0], self.user1.email)


class TeamViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.team = Team.objects.create(name="Team A")
        self.user1 = User.objects.create(email="user1@example.com", first_name="John", last_name="Doe")
        self.team.members.add(self.user1)
        self.url = reverse("teams:team-list")

    def test_list_teams(self):
        response = self.client.get(reverse("teams:team-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], self.team.name)
        self.assertEqual(response.data[0]["members"], [self.user1.email])

    def test_retrieve_team(self):
        url = reverse("teams:team-detail", kwargs={"pk": self.team.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.team.name)
        self.assertEqual(response.data["members"][0]["email"], self.user1.email)

    def test_create_team(self):
        data = {
            "name": "Team B",
            "members": [self.user1.id],
        }
        response = self.client.post(reverse("teams:team-list"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Team.objects.count(), 2)

    def test_update_team(self):
        url = reverse("teams:team-detail", kwargs={"pk": self.team.pk})
        data = {"name": "Updated Team A"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.team.refresh_from_db()
        self.assertEqual(self.team.name, "Updated Team A")

    def test_delete_team(self):
        url = reverse("teams:team-detail", kwargs={"pk": self.team.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Team.objects.count(), 0)
