from django.db import models
from papermanager.models import Paper

# Create your models here.
class PublishedPaper(models.Model):
    published_date=models.DateTimeField(auto_now_add=True)
    paper=models.OneToOneField(Paper)
    whitePaper=models.FileField(upload_to='uploads/%Y-%m-%d/')
    def author(self):
        return self.paper.author
    def __str__(self):
        return self.paper.name