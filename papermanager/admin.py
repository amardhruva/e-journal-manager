from django.contrib import admin
from papermanager.models import Paper, PaperVersion
from baseportal.models import PublishedPaper
from django.core.files.base import ContentFile

# Register your models here.
class PaperVersionInline(admin.TabularInline):
    model=PaperVersion
    fields=('name',)
    readonly_fields=('review_status',)

@admin.register(Paper)
class PaperAdmin(admin.ModelAdmin):
    list_display=('name', 'author', 'reviewer', 'public', "is_publishable")
    inlines=[
        PaperVersionInline,
    ]
    actions=['publish_papers']
    def publish_papers(self, request, queryset):
        for paper in queryset:
            if (not (paper.is_publishable())) or paper.public==True:
                continue
            approvedPaperVersion=paper.paperversion_set.get(reviewstatus__status="Y")
            paperFile=approvedPaperVersion.paperfiles_set.get()
            publishedPaper=PublishedPaper(paper=paper)
            publishedPaper.whitePaper.save(paperFile.filename,ContentFile(paperFile.filedata))
            publishedPaper.save()
    publish_papers.short_description = 'Publish selected Papers'