from django import forms

class ComicSearchForm(forms.Form):
    searchParam = forms.CharField(label='Search for comics by title, characters, or creators', max_length=255)