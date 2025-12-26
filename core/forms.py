from django import forms
from .models import Task
from jalali_date.widgets import AdminJalaliDateWidget
from jalali_date.fields import JalaliDateField
from jalali_date import date2jalali
from django.utils import timezone

class EditTaskForm(forms.ModelForm):
    reminder_date = JalaliDateField(label='تاریخ',widget=AdminJalaliDateWidget({'placeholder':date2jalali(timezone.now()).strftime('%Y/%m/%d')}))

    class Meta:
        model = Task
        exclude = ['user']
        labels = {
            'title':'عنوان',
            'status':'وضعیت',
        }


class TaskForm(forms.ModelForm):

    title = forms.CharField(label='عنوان',widget=forms.TextInput({'placeholder':'کار مورد نظر را وارد کنید'}))
    reminder_date = JalaliDateField(label='تاریخ',
                                    widget=AdminJalaliDateWidget({'placeholder':date2jalali(timezone.now()).strftime('%Y/%m/%d')}),
                                    required=False)

    class Meta:
        model = Task
        exclude = ['user','status']
