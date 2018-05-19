from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField()

class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes')