from django.db import models

from users import enums
from users.models import DoctorUser, PatientUser


class Appointment(models.Model):
    patient = models.ForeignKey(PatientUser, related_name="appointments", on_delete=models.CASCADE)
    department = models.CharField(max_length=20, choices=enums.Department.choices)
    doctor = models.ForeignKey(DoctorUser, on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.patient.first_name

    class Meta:
        ordering = ["pk"]

    @property
    def doctor_fullname(self):
        return f"{self.doctor.first_name} {self.doctor.last_name}"
