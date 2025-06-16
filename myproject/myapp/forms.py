from django import forms
from .models import Review

  
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['name', 'rating', 'text']
        labels = {
            'name': 'Ваше имя',
            'rating': 'Оценка',
            'text': 'Ваш отзыв'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'rating': forms.RadioSelect(choices=Review.RATING_CHOICES, attrs={'class': 'rating-input'}),
        }

