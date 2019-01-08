from django.contrib.auth.models import User, Group
from django.contrib.auth import get_user_model
User = get_user_model()
from rest_framework import viewsets

from aeon.models import (
    Organization
)
from aeon.serializers import (
    UserSerializer, GroupSerializer, OrganizationSerializer
)


class UserViewSet(viewsets.ModelViewSet):
  """
  API endpoint that allows users to be viewed or edited.
  """
  queryset = User.objects.all().order_by('-date_joined')
  serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
  """
  API endpoint that allows groups to be viewed or edited.
  """
  queryset = Group.objects.all()
  serializer_class = GroupSerializer


class OrganizationViewSet(viewsets.ModelViewSet):
  """
  API endpoint that allows organizations to be viewed or edited
  """
  queryset = Organization.objects.all()
  serializer_class = OrganizationSerializer
