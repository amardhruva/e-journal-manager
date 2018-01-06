from django.db import models
from papermanager.models import PaperVersion
from django.contrib.auth.models import User

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

