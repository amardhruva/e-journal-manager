from django.contrib import admin
from papermanager.models import Paper, PaperVersion

# Register your models here.
class PaperVersionInline(admin.TabularInline):
    model=PaperVersion
    fields=('name',)

@admin.register(Paper)
class PaperAdmin(admin.ModelAdmin):
    list_display=('name', 'author', 'reviewer', 'public')
    inlines=[
        PaperVersionInline,
    ]