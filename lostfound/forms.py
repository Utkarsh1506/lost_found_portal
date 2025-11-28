from django import forms
from .models import Item

class LostItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'category', 'color', 'brand', 'description', 'location_lost', 'date_lost', 'photo']
        widgets = {f: forms.TextInput(attrs={'class': 'form-control'}) for f in ['title','color','brand','location_lost']}
        widgets.update({
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'date_lost': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        })

class FoundItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'category', 'color', 'brand', 'description', 'location_found', 'date_found', 'photo']
        widgets = {f: forms.TextInput(attrs={'class': 'form-control'}) for f in ['title','color','brand','location_found']}
        widgets.update({
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'date_found': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        })
