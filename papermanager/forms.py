from django.forms.models import ModelForm
from papermanager.models import Paper, PaperVersion


class PaperForm(ModelForm):
    class Meta:
        model=Paper
        fields=("name","description")

class PaperVersionForm(ModelForm):
    class Meta:
        model=PaperVersion
        fields=("name","submissionType")