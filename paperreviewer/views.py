from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import View
from papermanager.models import PaperVersion, Paper, PaperFiles
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

# Create your views here.
class ReviewerProfileView(LoginRequiredMixin, View):
    def get(self, request):
        reviewPapers=Paper.objects.filter(reviewer=request.user)
        context={
            "reviewPapers":reviewPapers,
        }
        return render(request, "paperreviewer/profile.html", context)

class ReviewPaperView(LoginRequiredMixin, View):
    def get(self, request, paperslug):
        reviewPaper=get_object_or_404(Paper, slug=paperslug)
        if reviewPaper.reviewer != request.user:
            raise PermissionDenied
        paperVersions=PaperVersion.objects.filter(paper=reviewPaper)
        paperVersions=paperVersions.exclude(reviewstatus__status="W")
        context={
            "reviewPaper":reviewPaper,
            "paperVersions":paperVersions,
        }
        return render(request, "paperreviewer/reviewpaper.html", context)

def getPaperVersionReviewer(request, paperslug, versionslug):
    paper=get_object_or_404(Paper,slug=paperslug)
    if paper.reviewer != request.user:
            raise PermissionDenied
    versions=PaperVersion.objects.filter(paper=paper)
    version=get_object_or_404(versions,slug=versionslug)
    paperfiles=PaperFiles.objects.filter(paperversion=version)
    return paper,version,paperfiles

class ReviewPaperVersionView(LoginRequiredMixin, View):
    def get(self, request, paperslug, versionslug):
        paper,version,paperfiles=getPaperVersionReviewer(request, paperslug, versionslug)
        context={
            "paper":paper,
            "paperVersion":version,
            "paperFiles":paperfiles,
        }
        return render(request, "paperreviewer/reviewpaperversion.html", context)

class ReviewPaperAcceptedView(LoginRequiredMixin, View):
    def get(self, request, paperslug, versionslug):
        paper,version,paperfiles=getPaperVersionReviewer(request, paperslug, versionslug)
        reviewstatus=version.reviewstatus
        reviewstatus.status="Y"
        reviewstatus.save()
        return redirect("paperreviewer:reviewpaper",paperslug=paper.slug)

class ReviewPaperRejectedView(LoginRequiredMixin, View):
    def get(self, request, paperslug, versionslug):
        paper,version,paperfiles=getPaperVersionReviewer(request, paperslug, versionslug)
        reviewstatus=version.reviewstatus
        reviewstatus.status="N"
        reviewstatus.save()
        return redirect("paperreviewer:reviewpaper",paperslug=paper.slug)
        
    
        