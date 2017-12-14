from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.forms import SignUpForm, UserTypeForm

# Create your views here.

class ProfileView(LoginRequiredMixin,View):
    def get(self, request):
        return render(request, "accounts/profile.html")

class SignUpView(View):
    def post(self, request):
        context={
        "form" : SignUpForm(request.POST),
        "form2" : UserTypeForm(request.POST),
        }
        if all([context["form"].is_valid(),context["form2"].is_valid()]):
            user=context["form"].save(commit=False)
            user.is_active=False
            user.save()
            usertype=context["form2"].save(commit=False)
            usertype.user=user
            usertype.save()
            return render(request, 'registration/signup_success.html')
        return render(request, 'registration/signup.html', context)
    def get(self, request):
        context={
        "form" : SignUpForm(),
        "form2" : UserTypeForm(),
        }
        return render(request, 'registration/signup.html', context)