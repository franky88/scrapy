from django import forms
from .models import URLaddress

class URLaddressForm(forms.ModelForm):
    class Meta:
        model = URLaddress
        fields = ["url",]

        widgets = {
            'url': forms.TextInput(attrs={'class': 'form-control me-2', 'type': 'search', 'placeholder': 'Search URL', 'aria-label': 'Search'}),
        }

FORMAT_CHOICES = (
    ('xls', 'xls'),
    ('csv', 'csv'),
    ('json', 'json'),
)

class ProductFormat(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    format = forms.ChoiceField(choices=FORMAT_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))