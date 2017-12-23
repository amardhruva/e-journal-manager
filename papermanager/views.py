from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View
from papermanager.forms import PaperForm, PaperVersionForm
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
        
class AddPaperVersionView(LoginRequiredMixin, View):    
    def get(self, request, paperslug):
        paper=get_object_or_404(Paper,slug=paperslug)
        if paper.author != request.user:
            raise Http404
        form=PaperVersionForm()
        context={
            "paper":paper,
            "form":form,
        }
        return render(request, "papermanager/addpaperversion.html", context)
    def post(self, request, paperslug):
        paper=get_object_or_404(Paper,slug=paperslug)
        if paper.author != request.user:
            raise Http404
        form=PaperVersionForm(request.POST)
        if form.is_valid():
            version=form.save(commit=False)
            version.paper=paper
            version.save()
            return redirect("papermanager:editpaperversions",slug=paper.slug)
        context={
            "paper":paper,
            "form":form,
        }
        return render(request, "papermanager/addpaperversion.html", context)

class ShowPaperVersionView(LoginRequiredMixin, View):
    def get(self, request, paperslug, versionslug):
        paper=get_object_or_404(Paper,slug=paperslug)
        if paper.author != request.user:
            raise Http404
        versions=PaperVersion.objects.filter(paper=paper)
        version=get_object_or_404(versions,slug=versionslug)
        context={
            "paper":paper,
            "version":version,
        }
        return render(request, "papermanager/showpaperversion.html", context)

    

