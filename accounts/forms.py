from django import forms
from .models import User

class Signup_Form(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)


    class Meta:
        model = User
        fields = ['phone','fullname','password','confirm_password']
        labels = {
            'phone':'شماره تلفن',
            'fullname':'نام کاربری',
            'password':'کلمه عبور',
            'confirm_password':'تکرار کلمه عبور',
        }
    
    def clean_password2(self):
        p1 = self.cleaned_data.get('password')
        p2 = self.cleaned_data.get('confirm_password')
        if p1 != p2:
            raise forms.ValidationError('کلمه های عبور یکی نیستند')
        return p2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user