from django.contrib import admin

from appointments.models import Appointment


class AppointmentAdmin(admin.ModelAdmin):
    list_filter = ("department", "doctor", "patient")
    search_fields = ("patient__username", "doctor", "patient")
    list_display = ("patient", "department", "doctor", "date", "time", "created_at", "updated_at")


admin.site.register(Appointment, AppointmentAdmin)
