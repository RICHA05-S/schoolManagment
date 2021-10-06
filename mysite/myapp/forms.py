from django import forms
from .models import Profile,Subject


class UpdateForm(forms.ModelForm):

    class Meta:
        model=Profile
        fields='__all__'


class SubjectUpdateForm(forms.ModelForm):

    class Meta:
        model=Subject
        fields='__all__'