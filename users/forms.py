from django import forms
from django.contrib.auth.forms import UserCreationForm

from users import models


class SignUpForm(UserCreationForm):
    class Meta:
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        ]

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 != password2:
            raise forms.ValidationError("Passwords do not match.")

        return password2


class PatientSignUpForm(SignUpForm):
    class Meta(SignUpForm.Meta):
        model = models.PatientUser


class AdminSignUpForm(SignUpForm):
    class Meta(SignUpForm.Meta):
        model = models.AdminUser


class DoctorSignUpForm(SignUpForm):
    class Meta(SignUpForm.Meta):
        model = models.DoctorUser
