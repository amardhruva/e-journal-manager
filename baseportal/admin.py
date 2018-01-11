from django.contrib import admin
from papermanager.models import Paper, PaperVersion
from baseportal.models import PublishedPaper

# Register your models here.
@admin.register(PublishedPaper)
class FinalPaperAdmin(admin.ModelAdmin):
    list_display=("paper","author","published_date")