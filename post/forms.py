from django import forms
from django.contrib.auth import get_user_model

from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['subject', 'content', 'anonymous']
        labels = {
            "subject": "Title",
            "content": "Discussion",
        }
        widgets = {
            "content": forms.Textarea(attrs={'rows': 7, 'cols': 15})
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'anonymous']
        labels = {
            "content": "Your Reply"    
            }
        widgets = {
            "content": forms.Textarea(attrs={'rows': 7, 'cols': 15})
        }