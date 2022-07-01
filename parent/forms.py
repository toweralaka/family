from django import forms

from .models import ParentName, ChildName


class ParentForm(forms.ModelForm):
    class Meta:
        model = ParentName
        fields = '__all__'


class ChildForm(forms.ModelForm):
    dob = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD'}))
    class Meta:
        model = ChildName
        exclude = ('parent',)