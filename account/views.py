from typing import Any
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.http import HttpResponse
from django.shortcuts import resolve_url, redirect, render
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy
from django.views.generic import View
# Create your views here.

class LoginPage(LoginView):
    template_name = "accounts/login.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        ctx["title"] = gettext_lazy("Login")
        return ctx
    
    def form_invalid(self, form: AuthenticationForm) -> HttpResponse:
        form.add_error("password", gettext_lazy("Enter a valid credential"))
        form.add_error("username", gettext_lazy("Enter a valid credential"))
        return super().form_invalid(form)

    def get_success_url(self):
        return self.request.GET.get("next") or resolve_url("home:home")
    

class LogOutRedirect(View):
    template_name = "accounts/logout.html"

    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect("home:home")    

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, )
    