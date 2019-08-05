from django import forms
from .models import News


class CommentForms(forms.ModelForm):
    class Meta:
        model = News
        fields = ["news_comments"]