from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View
from papermanager.forms import PaperForm
from django.contrib.auth.mixins import LoginRequiredMixin
from papermanager.models import Paper, PaperVersion
from django.http.response import Http404

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

class EditPaperVersionsView(LoginRequiredMixin, View):
    def get(self, request, slug):
        paper=get_object_or_404(Paper,slug=slug)
        if paper.author != request.user:
            raise Http404
        versions=PaperVersion.objects.filter(paper=paper)
        context={
            "paper":paper,
            "paperversions":versions,
        }
        return render(request, "papermanager/editpaperversions.html", context)
        