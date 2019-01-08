from django.contrib.auth.models import User, Group
from django.contrib.auth import get_user_model
User = get_user_model()
from rest_framework import serializers

from .models import (Organization, System)


class UserSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = User
    fields = ('email', 'first_name', 'last_name', 'organization', 'groups',
    'last_login', 'date_joined', 'avatar')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Group
    fields = ('url', 'name')


class OrganizationSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Organization
    fields = ('id', 'name', 'description')


class SystemSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = System
    fields = ('name', 'organization', 'ip_address', 'description')
