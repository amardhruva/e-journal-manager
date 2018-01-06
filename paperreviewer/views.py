from django.shortcuts import render, get_object_or_404
from django.views.generic.base import View
from papermanager.models import PaperVersion, Paper
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
        