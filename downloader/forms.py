from django import forms

class VideoDownloaderFrom(forms.Form):
    url = forms.URLField(label='Video URL', max_length=200)