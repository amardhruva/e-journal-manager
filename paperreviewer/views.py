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


        