import uuid

#from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

from .managers import UserManager

STATE_CHOICES = (
    ("OK", "OKAY"),
    ("FAIL", "FAILURE"),
    ("WARN", "WARN"),
)


class Organization(models.Model):

    """General company/org association holder."""

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        app_label = 'aeon'

    def __str__(self):
        return self.name


class CustomUser(AbstractBaseUser, PermissionsMixin):

    """ Override for User """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    last_login = models.DateTimeField(auto_now=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    organization = models.ForeignKey(Organization, null=True, on_delete=models.PROTECT)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        app_label = 'aeon'
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.email


class System(models.Model):

    """ Container for a system """

    name = models.CharField(max_length=254)
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT)
    ip_address = models.GenericIPAddressField()
    description = models.TextField(blank=True)

    class Meta:
        app_label = 'aeon'
        unique_together = ('name', 'organization',)

    def __str__(self):
        return self.name


class Service(models.Model):

    """ Container for service """

    name = models.CharField(max_length=254)
    system = models.ForeignKey(System, on_delete=models.PROTECT)

    class Meta:
        app_label = 'aeon'
        unique_together = ('name', 'system',)

    def __str__(self):
        return self.name


class Application(models.Model):

    """ Container for application """

    name = models.CharField(max_length=254)
    system = models.ForeignKey(System, on_delete=models.PROTECT)

    class Meta:
        app_label = 'aeon'
        unique_together = ('name', 'system',)

    def __str__(self):
        return self.name


class Status(models.Model):

    """ Status record for service events """

    created = models.DateTimeField(auto_now_add=True)
    system = models.ForeignKey(System, on_delete=models.PROTECT)
    application = models.ForeignKey(Application, on_delete=models.PROTECT, blank=True)
    service = models.ForeignKey(Service, on_delete=models.PROTECT, blank=True)
    state = models.CharField(choices=STATE_CHOICES, default='OKAY', max_length=100)
    description = models.TextField(blank=True)

    class Meta:
        app_label = 'aeon'
        ordering = ('created',)

    def __str__(self):
        return self.description
