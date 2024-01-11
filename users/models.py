from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.core.validators import (
    EmailValidator,
    validate_image_file_extension,
)
from django.db import models
from django_cleanup import cleanup

from users.enums import UserRole
from users.managers import (
    AdminUserManager,
    DoctorUserManager,
    PatientUserManager,
    UserProfileManager,
)
from users.utils.media_path import set_avatar_path
from users.validators.cpf_validator import validate_cpf
from users.validators.username_validator import validate_username


class User(AbstractUser, PermissionsMixin):
    DEFAULT_ROLE = UserRole.ADMIN

    username = models.CharField(max_length=30, validators=[validate_username], unique=True)
    email = models.EmailField(validators=[EmailValidator], unique=True)
    role = models.CharField(max_length=7, choices=UserRole.choices)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    REQUIRED_FIELDS = ["first_name", "last_name", "email"]

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.DEFAULT_ROLE
            return super().save(*args, **kwargs)


@cleanup.select
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cpf = models.CharField(max_length=14, validators=[validate_cpf])
    date_of_birth = models.DateField()
    avatar = models.ImageField(
        validators=[validate_image_file_extension],
        upload_to=set_avatar_path,
        null=True,
        blank=True,
    )
    updated_at = models.DateTimeField(auto_now=True, null=True)
    objects = UserProfileManager()

    class Meta:
        abstract = True
        permissions = (("can view profiles", "Can view all profiles"),)


class AdminUser(User):
    DEFAULT_ROLE = UserRole.ADMIN
    objects = AdminUserManager()

    class Meta:
        proxy = True


class DoctorUser(User):
    DEFAULT_ROLE = UserRole.DOCTOR
    objects = DoctorUserManager()

    class Meta:
        proxy = True


class PatientUser(User):
    DEFAULT_ROLE = UserRole.PATIENT
    objects = PatientUserManager()

    class Meta:
        proxy = True


class PatientUserProfile(UserProfile):
    pass


class AdminUserProfile(UserProfile):
    pass


class DoctorUserProfile(UserProfile):
    crm = models.CharField(max_length=14)
