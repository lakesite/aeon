import os
import uuid

from django.db import migrations, models
import django.db.models.deletion

import aeon.managers
from aeon.models import CustomUser


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    def generate_superuser(apps, schema_editor):
        from django.contrib.auth.models import User

        DJANGO_DB_NAME = os.environ.get('DJANGO_DB_NAME', "aeon")
        DJANGO_SU_EMAIL = os.environ.get('DJANGO_SU_EMAIL', "aeon@localhost")
        DJANGO_SU_PASSWORD = os.environ.get('DJANGO_SU_PASSWORD', "password123")

        superuser = CustomUser.objects.create_superuser(
            email=DJANGO_SU_EMAIL,
            password=DJANGO_SU_PASSWORD)

        superuser.save()

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('first_name', models.CharField(blank=True, max_length=255)),
                ('last_name', models.CharField(blank=True, max_length=255)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('last_login', models.DateTimeField(auto_now=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='avatars/')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', aeon.managers.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('state', models.CharField(choices=[('OK', 'OKAY'), ('FAIL', 'FAILURE'), ('WARN', 'WARN')], default='OKAY', max_length=100)),
                ('description', models.TextField(blank=True)),
                ('application', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to='aeon.Application')),
                ('service', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to='aeon.Service')),
            ],
            options={
                'ordering': ('created',),
            },
        ),
        migrations.CreateModel(
            name='System',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=254)),
                ('ip_address', models.GenericIPAddressField()),
                ('description', models.TextField(blank=True)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='aeon.Organization')),
            ],
        ),
        migrations.AddField(
            model_name='status',
            name='system',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='aeon.System'),
        ),
        migrations.AddField(
            model_name='service',
            name='system',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='aeon.System'),
        ),
        migrations.AddField(
            model_name='application',
            name='system',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='aeon.System'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='organization',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='aeon.Organization'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
        migrations.AlterUniqueTogether(
            name='system',
            unique_together={('name', 'organization')},
        ),
        migrations.AlterUniqueTogether(
            name='service',
            unique_together={('name', 'system')},
        ),
        migrations.AlterUniqueTogether(
            name='application',
            unique_together={('name', 'system')},
        ),
        migrations.RunPython(generate_superuser),
    ]
