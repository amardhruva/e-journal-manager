from django.forms.models import ModelForm
from papermanager.models import Paper


class PaperForm(ModelForm):
    class Meta:
        model=Paper
        fields=("name","description")