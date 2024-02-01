from django.shortcuts import render, redirect
from .forms import LoginFormAuthentication, PasswordChangeForm
from django.contrib.auth.views import LoginView, PasswordChangeView, LogoutView
from django.urls import reverse_lazy



class UserLoginView(LoginView):
    form_class = LoginFormAuthentication
    template_name = "accounts/login.html"
    success_url = "/"

    def form_valid(self, form):
        response = super().form_valid(form)
        return redirect(self.success_url)
    

# class PasswordChange(PasswordChangeView):
#     form_class = PasswordChangeForm
#     template_name = "accounts/change-passwords.html"
#     success_url = reverse_lazy('login')


class UserLogout(LogoutView):
    template_name = "accounts/login-user.html"

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return redirect("login")