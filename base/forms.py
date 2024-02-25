from django import forms
from .models import Verification

"""secure verification form"""

class VerificationForm(forms.ModelForm):
    class Meta:
        model = Verification
        fields = ['nin_front', 'nin_back', 'proclaim_video', 'full_picture']

