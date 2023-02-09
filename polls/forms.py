from django import forms
from .models import Topic, Entry, Subscribe


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['text']
        labels = {'text': ''}


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text': ''}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}


class SubsForm(forms.ModelForm):
    class Meta:
        model = Subscribe
        fields = ['subs']
        labels = {'subs': ''}