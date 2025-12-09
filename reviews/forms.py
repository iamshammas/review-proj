from django import forms
from .models import Review

class AdvisorReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['date', 'intern_name', 'lesson_name', 'preferred_reviewer', 'remarks']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'intern_name': forms.TextInput(attrs={'placeholder': 'Enter intern name'}),
            'lesson_name': forms.TextInput(attrs={'placeholder': 'Eg: React W1'}),
            'remarks': forms.Textarea(attrs={
                'placeholder': 'Enter any additional remarks or notes...',
                'rows': 3,
                'style': 'resize: vertical; min-height: 100px;'
            }),
        }

class ReviewUpdateForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['date', 'start_time', 'google_meet_link', 'assigned_reviewer', 'status']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'google_meet_link': forms.TextInput(attrs={'placeholder': 'https://meet.google.com/...'}),
        }