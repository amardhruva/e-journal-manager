from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View
from papermanager.forms import PaperForm, PaperVersionForm, UploadFileForm
from django.contrib.auth.mixins import LoginRequiredMixin
from papermanager.models import Paper, PaperVersion, PaperFiles
from django.http.response import Http404, HttpResponseRedirect, HttpResponse
import mimetypes
from django.forms.forms import Form
from paperreviewer.models import ReviewStatus
from django.core.exceptions import PermissionDenied
import re

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
            reviewstatus=ReviewStatus()
            reviewstatus.paperversion=version
            reviewstatus.save()
            return redirect("papermanager:editpaperversions",slug=paper.slug)
        context={
            "paper":paper,
            "form":form,
        }
        return render(request, "papermanager/addpaperversion.html", context)

def handle_uploaded_file(file, paperversion):
    filedata=file.file.read()
    filename=re.sub(r'[^.\-_\w]', '', file.name)
    paperfile=PaperFiles(filename=filename, filedata=filedata, paperversion=paperversion)
    paperfile.save()

def getPaperVersion(request, paperslug, versionslug):
    paper=get_object_or_404(Paper,slug=paperslug)
    if paper.author != request.user:
            raise PermissionDenied
    versions=PaperVersion.objects.filter(paper=paper)
    version=get_object_or_404(versions,slug=versionslug)
    paperfiles=PaperFiles.objects.filter(paperversion=version)
    return paper,version,paperfiles



class ShowPaperVersionView(LoginRequiredMixin, View):
    def get(self, request, paperslug, versionslug):
        paper,version,paperfiles=getPaperVersion(request, paperslug, versionslug)
        uploadform=UploadFileForm()
        context={
            "paper":paper,
            "version":version,
            "paperfiles":paperfiles,
            "uploadform":uploadform,
        }
        return render(request, "papermanager/showpaperversion.html", context)
    def post(self, request, paperslug, versionslug):
        paper,version,paperfiles=getPaperVersion(request, paperslug, versionslug)
        uploadform=UploadFileForm(request.POST, request.FILES)
        if uploadform.is_valid():
            handle_uploaded_file(request.FILES['file'], version)
            return redirect('papermanager:showpaperversion',paperslug=paperslug,versionslug=versionslug)
        context={
            "paper":paper,
            "version":version,
            "paperfiles":paperfiles,
            "uploadform":uploadform,
        }
        return render(request, "papermanager/showpaperversion.html", context)

class SubmitPaperView(LoginRequiredMixin, View):
    def get(self, request, paperslug, versionslug):
        paper,version,paperfiles=getPaperVersion(request, paperslug, versionslug)
        form=Form()
        return render(request, "papermanager/submitpaper.html", {"form":form})
    def post(self, request, paperslug, versionslug):
        paper,version,paperfiles=getPaperVersion(request, paperslug, versionslug)
        form=Form(request.POST)
        if form.is_valid():
            reviewstatus=version.reviewstatus
            if reviewstatus.status=="W":
                reviewstatus.status="P"
                reviewstatus.save()
            return redirect('papermanager:showpaperversion',paperslug=paperslug,versionslug=versionslug)
        return render(request, "papermanager/submitpaper.html", {"form":form})
        

class DownloadFile(LoginRequiredMixin, View):
    def get(self, request, paperslug, versionslug, fileslug):
        paper,version,paperfiles=getPaperVersion(request, paperslug, versionslug)
        fileObject=get_object_or_404(paperfiles, slug=fileslug)
        filename=fileObject.filename
        mime=mimetypes.guess_type(filename)
        if mime[0] is None:
            mime="text/plain"
        else:
            mime=mime[0]
        response=HttpResponse(fileObject.filedata,content_type=mime)
        response['Content-Disposition'] = 'attachment; filename={}'.format(filename)
        return response
        
        
        

