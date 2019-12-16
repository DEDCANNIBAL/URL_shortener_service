from django.contrib.auth import login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views import View
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class RegisterFormView(FormView):
    form_class = UserCreationForm
    template_name = "register.html"
    success_url = "/register"

    def form_valid(self, form):
        form.save()
        messages.add_message(self.request, messages.INFO, 'Account created successfully.')
        return super(RegisterFormView, self).form_valid(form)


class LoginFormView(FormView):
    form_class = AuthenticationForm
    template_name = 'login.html'
    success_url = "/"


    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return super(LoginFormView, self).form_valid(form)


class LogoutView(View):
    template_name = "/"

    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(self.template_name)
