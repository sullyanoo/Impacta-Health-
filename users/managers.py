from django.contrib.auth.models import BaseUserManager
from django.db import models
from django.db.models.query import QuerySet

from users.enums import UserRole


class UserManager(BaseUserManager, models.Manager):
    def create_user(
        self,
        username,
        first_name,
        last_name,
        email,
        password,
        **other_fields,
    ):
        email = self.normalize_email(email)
        account = self.model(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            **other_fields,
        )
        account.set_password(password)
        account.save(using=self._db)
        return account

    def create_superuser(
        self,
        username,
        first_name,
        last_name,
        email,
        password,
        **other_fields,
    ):
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_active", True)

        return self.create_user(
            username,
            first_name,
            last_name,
            email,
            password,
            **other_fields,
        )

    def get_by_natural_key(self, username):
        return self.get(username=username)


class AdminUserManager(UserManager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(role=UserRole.ADMIN)

    def get_by_natural_key(self, username):
        return self.get(username=username)


class DoctorUserManager(UserManager):
    def get_queryset(self, *args, **kwargs) -> QuerySet:
        return super().get_queryset().filter(role=UserRole.DOCTOR)

    def get_by_natural_key(self, username):
        return self.get(username=username)


class PatientUserManager(UserManager):
    def get_queryset(self, *args, **kwargs) -> QuerySet:
        return super().get_queryset().filter(role=UserRole.PATIENT)

    def get_by_natural_key(self, username):
        return self.get(username=username)


class UserProfileManager(models.Manager):
    def get_by_natural_key(self, user):
        return self.get(user=user)
