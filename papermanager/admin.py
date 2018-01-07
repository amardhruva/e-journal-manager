from django.contrib import admin
from papermanager.models import Paper, PaperVersion

# Register your models here.
class PaperVersionInline(admin.TabularInline):
    model=PaperVersion

@admin.register(Paper)
class PaperAdmin(admin.ModelAdmin):
    inlines=[
        PaperVersionInline,
    ]