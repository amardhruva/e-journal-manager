from django.db import models
from django.contrib.auth.models import User

USER_TYPE_CHOICES=(
    ('R',"Reviewer"),
    ('S',"Submitter")
    
)
# Create your models here.
class UserType(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    type=models.CharField(max_length=1,choices=USER_TYPE_CHOICES)
    def __str__(self):
        return self.get_type_display()