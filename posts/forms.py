from django import forms
from .models import Post
from articles.models import Article
from django.shortcuts import get_object_or_404



class CreatePostSpecificForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['message', 'article']

    def __init__(self, *args, **kwargs):
        article_id = kwargs.pop('article_id', None)
        super().__init__(*args, **kwargs)

        if article_id is not None:
            article = get_object_or_404(Article, pk=article_id)
            # Set the 'article' field as hidden and set the initial value
            self.fields['article'].widget = forms.HiddenInput()
            self.fields['article'].initial = article