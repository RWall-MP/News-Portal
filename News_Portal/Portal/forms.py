from django import forms
from .models import Post
from django.core.exceptions import ValidationError


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'type',
            'title',
            'category',
            'text',
        ]

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        text = cleaned_data.get('text')
        if title is not None and len(title) > 32:
            raise ValidationError({
                'title': 'Название не может превышать 32 символа.'
            })
        if title == text:
            raise ValidationError({
                'text': 'Содержание названия и текста статьи/новости не должно совпадать.'
            })
        return cleaned_data
