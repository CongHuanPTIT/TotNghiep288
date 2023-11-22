from django import forms


class CommentForm(forms.Form):
    comment = forms.CharField(label="", widget=forms.Textarea(attrs={'class': 'form-control',
                                                                     'placeholder': 'Leave your comment'}))
