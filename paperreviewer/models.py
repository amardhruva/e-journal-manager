from django.db import models
from papermanager.models import PaperVersion, PaperFiles
from django.contrib.auth.models import User
from slugger.fields import AutoSlugField
from django.utils.crypto import get_random_string

REVIEW_STATUS_CHOICES=(
    ('W',"Not yet submitted"),
    ('P',"Review Pending"),
    ('Y',"Accepted"),
    ('N',"Rejected"),
)

# Create your models here.
class ReviewStatus(models.Model):
    paperversion=models.OneToOneField(PaperVersion)
    status=models.CharField(max_length=1, choices=REVIEW_STATUS_CHOICES, default='W')
    def __str__(self):
        return self.get_status_display()

class ExposedPDF(models.Model):
    pdf_file=models.ForeignKey(PaperFiles)
    randomseed=models.CharField(max_length=20,default=get_random_string(length=20))
    slug=AutoSlugField(populate_from="randomseed", unique=True)
    creation_time=models.DateTimeField(auto_now=True)
    

