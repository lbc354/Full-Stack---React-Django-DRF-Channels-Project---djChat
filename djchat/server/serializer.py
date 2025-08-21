from rest_framework import serializers
from server.models import Category, Server, Channel


class ServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Server
        fields = "__all__"
