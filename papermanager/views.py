from django.shortcuts import render, redirect
from django.views.generic.base import View
from papermanager.forms import PaperForm
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class CreatePaperView(LoginRequiredMixin, View):
    def get(self, request):
        context={
            "form":PaperForm(),
        }
        return render(request, "papermanager/createpaper.html", context)
    
    def post(self, request):
        form=PaperForm(request.POST)
        if form.is_valid():
            paper=form.save(commit=False)
            paper.author=request.user
            paper.save()
            return redirect("accounts:profile")
        
        context={
            "form":form,
        }
        return render(request, "papermanager/createpaper.html", context)