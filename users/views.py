from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from users.forms import AdminSignUpForm, DoctorSignUpForm, PatientSignUpForm
from users.models import AdminUser, DoctorUser, PatientUser, User
from users.validators.username_validator import validate_username


class SignUpView(View):
    user_model = None

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if request.method == "POST":
            if form.is_valid():
                username = form.cleaned_data["username"]
                first_name = form.cleaned_data["first_name"]
                last_name = form.cleaned_data["last_name"]
                email = form.cleaned_data["email"]
                password = form.cleaned_data["password2"]

                self.user_model.objects.create_user(
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=password,
                )
                auth_user = authenticate(request, username=username, password=password)
                if auth_user:
                    login(request, auth_user)

                return redirect("appointments:list")
            else:
                errors = form.errors.as_json()
                if errors:
                    return HttpResponse(errors, status=400, content_type="application/json")
        return render(request, self.template_name, {"form": form})


class LoginView(View):
    template_name = "login.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("appointments:index")
        else:
            return render(request, self.template_name, {"error_message": "Credenciais inválidas"})


def custom_logout(request):
    logout(request)
    return redirect("appointments:index")


class PatientSignUpView(SignUpView):
    user_model = PatientUser
    template_name = "patient_signup.html"
    form_class = PatientSignUpForm


class AdminSignUpView(SignUpView):
    user_model = AdminUser
    template_name = "admin_signup.html"
    form_class = AdminSignUpForm


class DoctorSignUpView(SignUpView):
    user_model = DoctorUser
    template_name = "doctor_signup.html"
    form_class = DoctorSignUpForm


@require_POST
@csrf_exempt
def signup_verify(request):
    username = request.POST.get("username")
    email = request.POST.get("email")

    username_exists = False
    email_exists = User.objects.filter(email=email).exists()

    username_error = ""

    if username is not None and username.strip():
        try:
            validate_username(username)
            username_exists = User.objects.filter(username=username).exists()
        except ValidationError as e:
            username_error = e.messages[0] if e.messages else ""

    data = {"username_exists": username_exists, "email_exists": email_exists, "username_error": username_error}
    return JsonResponse(data)


@require_POST
@csrf_exempt
def login_verify(request):
    username = request.POST.get("username")
    password = request.POST.get("password")

    user = authenticate(request, username=username, password=password)

    if user is not None:
        if user.is_active:
            login(request, user)
            return JsonResponse({"success": True})
    return JsonResponse({"success": False})
