from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control bg-dark text-light border-secondary', 
                'rows': 3, 
                'placeholder': 'Napiš svůj názor k článku...'
            }),
        }
        labels = {
            'content': '',
        }