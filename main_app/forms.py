from django.forms import ModelForm
from . models import Tuning

class TuningForm(ModelForm):
    class Meta:
        model = Tuning
        fields = ['date', 'shop']

