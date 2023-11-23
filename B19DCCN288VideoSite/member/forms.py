from django import forms
from .models import Member
from datetime import datetime


class MemberForm(forms.Form):
    name = forms.CharField(label="Name", widget=forms.TextInput(attrs={'placeholder': 'Your name'}), max_length=50)
    date_of_birth = forms.DateField(label="Date of birth",
                                    widget=forms.DateInput(attrs={'type': 'date', 'max': datetime.now().date()}))
    other = forms.CharField(label="Introduction", widget=forms.Textarea(attrs={'other': 'profile_description'}))
    profile_image = forms.ImageField(required=False, error_messages={'invalid': "Image files only"})

    def clean(self):
        self.cleaned_data = super().clean()
        profile_image = self.cleaned_data.get('profile_image')
        if not profile_image:
            self.cleaned_data['profile_image'] = 'uploads/profile_images/default.jpg'

    def signup(self, request, user):
        user.save()
        member_profile = Member()
        member_profile.user = user
        member_profile.name = self.cleaned_data['name']
        member_profile.date_of_birth = self.cleaned_data['date_of_birth']
        member_profile.other = self.cleaned_data['other']
        member_profile.profile_image = self.cleaned_data['profile_image']
        member_profile.save()
