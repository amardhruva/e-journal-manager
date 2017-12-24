from django.forms.models import ModelForm
from papermanager.models import Paper, PaperVersion
from django.forms.forms import Form
from django.forms.fields import FileField


class PaperForm(ModelForm):
    class Meta:
        model=Paper
        fields=("name","description")

class PaperVersionForm(ModelForm):
    class Meta:
        model=PaperVersion
        fields=("name","submissionType")

class UploadFileForm(Form):
    file=FileField()