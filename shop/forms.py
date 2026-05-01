from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Review, UserProfile, SavedAddress


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'title', 'comment']
        widgets = {
            'rating': forms.RadioSelect(choices=Review.RATING_CHOICES),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Review title'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Share your experience...',
                'rows': 5
            }),
        }


class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=150, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = UserProfile
        fields = ['phone', 'bio', 'avatar']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+91 XXXXXXXXXX'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Tell us about yourself...', 'rows': 3}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
        }


class SavedAddressForm(forms.ModelForm):
    class Meta:
        model = SavedAddress
        fields = ['label', 'full_name', 'phone', 'address_line1', 'address_line2', 'city', 'state', 'pincode', 'is_default']
        widgets = {
            'label': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Home, Office'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address_line1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Street address'}),
            'address_line2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apt, suite, etc. (optional)'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'pincode': forms.TextInput(attrs={'class': 'form-control'}),
            'is_default': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
