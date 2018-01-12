from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import View
from papermanager.models import PaperVersion, Paper, PaperFiles
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied, SuspiciousOperation
import mimetypes
from django.http.response import HttpResponse
from papermanager.views import handle_uploaded_file
from paperreviewer.models import ExposedPDF
import requests
from django.urls.base import reverse

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
        if reviewstatus.status=="P":
            reviewstatus.status="Y"
            reviewstatus.save()
        return redirect("paperreviewer:reviewpaper",paperslug=paper.slug)

class ReviewPaperRejectedView(LoginRequiredMixin, View):
    def get(self, request, paperslug, versionslug):
        paper,version,paperfiles=getPaperVersionReviewer(request, paperslug, versionslug)
        reviewstatus=version.reviewstatus
        if reviewstatus.status=="P":
            reviewstatus.status="N"
            reviewstatus.save()
        return redirect("paperreviewer:reviewpaper",paperslug=paper.slug)
    def post(self, request, paperslug, versionslug):
        paper,version,paperfiles=getPaperVersionReviewer(request, paperslug, versionslug)
        reviewstatus=version.reviewstatus
        if reviewstatus.status=="P":
            reviewstatus.status="N"
            reviewstatus.save()
        file=request.FILES.get('file')
        if file is None:
            raise SuspiciousOperation("File Error")
        handle_uploaded_file(file, version, True)
        return redirect("paperreviewer:reviewpaper",paperslug=paper.slug)

class ReviewDownloadFileView(LoginRequiredMixin, View):
    def get(self, request, paperslug, versionslug, fileslug):
        paper,version,paperfiles=getPaperVersionReviewer(request, paperslug, versionslug)
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

class EditPDFView(LoginRequiredMixin, View):   
    def get(self, request, paperslug, versionslug, fileslug):
        paper,version,paperfiles=getPaperVersionReviewer(request, paperslug, versionslug)
        fileObject=get_object_or_404(paperfiles, slug=fileslug)
        filename=fileObject.filename  
        exposed_pdf=ExposedPDF(pdf_file=fileObject)
        exposed_pdf.save()
        
        pdfreturnurl=reverse('paperreviewer:exposedpdfrecieve', kwargs={"fileslug":exposed_pdf.slug})
        secret="dummy" #implement this
        context={
            "paper":paper,
            "paperVersion":version,
            "fileobject":fileObject,
            "pdfreturnurl":pdfreturnurl,
            "exposedpdf":exposed_pdf,
        }
        return render(request, "paperreviewer/editpaperfile.html", context)


class ExposedPDFRecieve(LoginRequiredMixin, View):
    def get(self, request, fileslug):
        file=get_object_or_404(ExposedPDF, slug=fileslug)
        fileObject=file.pdf_file
        paperVersion=fileObject.paperversion
        paper=paperVersion.paper
        
        if paper.reviewer!=request.user:
            raise PermissionDenied
        
        
        secret_data=request.GET.get('data')
        delete_link=request.GET.get('delete_link_base64')
        output_file=request.GET.get('path_pdf_output')
        resp=requests.get(output_file)
        
        newfile=PaperFiles(paperversion=paperVersion, filename=fileObject.filename+"-reply",
                           filedata=resp.content, from_reviewer=True)
        newfile.save()
        return redirect('paperreviewer:reviewpaperreject', paperslug=paper.slug, versionslug=paperVersion.slug)

        