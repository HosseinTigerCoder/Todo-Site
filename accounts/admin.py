from django.contrib import admin
from .models import User,Profile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.db.models import Count

# Register your models here.
class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput,label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput,label='Confirm Password')
    
    class Meta:
        model = User
        fields = ['phone','fullname']
    
    def clean_password2(self):
        p1 = self.cleaned_data.get('password1')
        p2 = self.cleaned_data.get('password2')
        if p1 != p2:
            raise forms.ValidationError('کلمه های عبور یکی نیستند')
        return p2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ["phone", "fullname", "password", "is_active", "is_staff"]

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # model = User
    add_form = UserCreationForm
    # form = UserChangeForm

    list_display = ['fullname','phone','is_staff','is_superuser']
    search_fields = ['fullname','phone']
    ordering = ["-is_superuser",'-id']

    fieldsets = (
        (None,{"fields":('phone','password')}),
        ('Personal Info',{"fields":('fullname','email')}),
        ('Permissions',{"fields":("is_active", "is_staff", "is_superuser", "groups", "user_permissions")})
    )

    add_fieldsets = (
        (None,{
         "classes":('wide',),
         "fields":('phone','fullname','email','password1','password2')
         }),
    )

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user','All_tasks','completed']

    def All_tasks(self,profile):
        return  profile.user.tasks.count()

    def completed(self,profile):
        return profile.user.tasks.filter(status=True).count()

