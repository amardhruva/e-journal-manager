from django.contrib import admin
from papermanager.models import Paper, PaperVersion

# Register your models here.
admin.site.register(Paper)
admin.site.register(PaperVersion)