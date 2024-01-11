from django.urls import path

# Import views
from . import views

app_name = "appointments"

urlpatterns = [
    path("", views.index, name="index"),
    path("appointments/schedule", views.CreateAppointmentView.as_view(), name="schedule"),
    path("appointments/reschedule/<int:pk>/", views.RescheduleAppointmentView.as_view(), name="reschedule"),
    path('appointments/delete/<int:pk>/', views.delete_appointment, name='delete'),
    path("appointments/list", views.ListAppointmentsView.as_view(), name="list"),
]
