from django import forms
from .models import Review, Intern, Lesson

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['date', 'intern', 'lesson', 'preferred_reviewer']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and hasattr(user, 'advisor'):
            self.fields['intern'].queryset = Intern.objects.filter(advisor=user.advisor)

class ReviewUpdateForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['date', 'start_time', 'google_meet_link', 'assigned_reviewer', 'status']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
        } 