from django.db import models
from papermanager.models import PaperVersion
from django.contrib.auth.models import User

REVIEW_STATUS_CHOICES=(
    ('P',"Review Pending"),
    ('Y',"Accepted"),
    ('N',"Rejected"),
)

# Create your models here.
class ReviewStatus(models.Model):
    paperversion=models.OneToOneField(PaperVersion)
    status=models.CharField(max_length=1, choices=REVIEW_STATUS_CHOICES)

