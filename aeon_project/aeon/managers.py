from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password=None, is_staff=False, is_admin=False, is_active=False, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('User must have an email address')
        if not password:
            raise ValueError('User must have a password')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.is_staff = is_staff
        user.is_admin = is_admin
        user.is_active = is_active
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_staffuser(self, email, password=None):
        return self._create_user(
            email,
            password=password,
            is_staff=True,
            is_active=True
        )

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, is_staff=True, is_admin=True, is_active=True, **extra_fields)
