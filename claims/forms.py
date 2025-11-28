from django import forms
from .models import Claim

class ClaimForm(forms.ModelForm):
    class Meta:
        model = Claim
        fields = ['claim_type', 'description', 'proof_text', 'proof_file']
        widgets = {
            'claim_type': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'proof_text': forms.Textarea(attrs={'class': 'form-control'}),
            'proof_file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
