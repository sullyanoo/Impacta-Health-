from django import forms

from appointments.models import Appointment


class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ["department", "doctor", "date", "time"]


class RescheduleForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ["date", "time"]
