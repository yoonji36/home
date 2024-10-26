from django import forms
from .models import User

class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['id', 'password', 'blood_sugar_target', 'height', 'weight']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    id = forms.CharField(label='아이디', max_length=50)
    password = forms.CharField(widget=forms.PasswordInput, label='비밀번호')
