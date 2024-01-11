from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from appointments.forms import RescheduleForm, ScheduleForm
from appointments.models import Appointment


def index(request):
    return render(request, "appointments/index.html")


class CreateAppointmentView(View):
    template_name = "appointments/schedule.html"
    form_class = ScheduleForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user
            appointment.save()
            return redirect("appointments:list")
        else:
            errors = form.errors.as_json()
            if errors:
                return HttpResponse(errors, status=400, content_type="application/json")
        return render(request, self.template_name, {"form": form})


class RescheduleAppointmentView(View):
    template_name = "appointments/reschedule.html"
    form_class = RescheduleForm

    def get(self, request, pk, *args, **kwargs):
        appointment = get_object_or_404(Appointment, pk=pk)
        form = self.form_class(instance=appointment)
        return render(request, self.template_name, {"form": form, "appointment": appointment})

    def post(self, request, pk, *args, **kwargs):
        appointment = get_object_or_404(Appointment, pk=pk)
        form = self.form_class(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect("appointments:list")
        else:
            errors = form.errors.as_json()
            if errors:
                return HttpResponse(errors, status=400, content_type="application/json")
        return render(request, self.template_name, {"form": form})
    


def delete_appointment(request, pk):
    appointment = get_object_or_404(Appointment, id=pk)
    appointment.delete()
    return redirect('appointments:list')


@method_decorator(login_required(login_url="/users/login/"), name="dispatch")
class ListAppointmentsView(View):
    def get(self, request):
        appointments = None

        if request.user:
            appointments = Appointment.objects.filter(patient=request.user)

        context = {
            "appointments": appointments,
        }

        return render(request, "appointments/appointments.html", context)


def reschedule(request):
    return render(request, "appointments/reschedule.html")
