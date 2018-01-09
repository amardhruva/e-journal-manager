from django.db import models
from papermanager.models import Paper

# Create your models here.
class FinalPaper(models.Model):
    publishedDate=models.DateTimeField(auto_now_add=True)
    paper=models.OneToOneField(Paper)
    whitePaper=models.FileField(upload_to='uploads/%Y-%m-%d/')