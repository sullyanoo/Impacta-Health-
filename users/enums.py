from django.db import models
from django.utils.translation import gettext_lazy as _


class UserRole(models.TextChoices):
    ADMIN = "ADMIN"
    DOCTOR = "DOCTOR"
    PATIENT = "PATIENT"


class Department(models.TextChoices):
    PSYCHOLOGY = _("PSYCHOLOGY"), _("Psicologia")
    NEUROLOGIST = _("NEUROLOGIST"), _("Neurologista")
    PEDIATRICIAN = _("PEDIATRICIAN"), _("Pediatra")
    DENTISTRY = _("DENTISTRY"), _("Odontologia")
    OPHTHALMOLOGIST = _("OPHTHALMOLOGIST"), _("Oftalmologista")
    GENERAL_PRACTITIONER = _("GENERAL_PRACTITIONER"), _("Clínico Geral")
