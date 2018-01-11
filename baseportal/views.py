from django.shortcuts import render
from baseportal.models import PublishedPaper

# Create your views here.
def homepageView(request):
    publishedPapers=PublishedPaper.objects.all()
    context={
        "papers":publishedPapers,
    }
    return render(request, "baseportal/homepage.html", context)