from django.contrib import admin
from .models import Task
from jalali_date.admin import ModelAdminJalaliMixin
from jalali_date import date2jalali
# Register your models here.


@admin.register(Task)
class TaskAdmin(ModelAdminJalaliMixin,admin.ModelAdmin):
    list_display = ['title','status','user','reminder_date_jalali']
    actions = ['complete_tasks','uncomplete_tasks']
    list_filter = ['user']

    def reminder_date_jalali(self,obj):
        if obj.reminder_date:
            return date2jalali(obj.reminder_date).strftime('%Y/%m/%d')
        return '-'
    
    @admin.action(description='علامت زدن به عنوان انجام شده')
    def complete_tasks(self,request,queryset):
        queryset.update(status=True)
        
    @admin.action(description='علامت زدن به عنوان انجام نشده')
    def uncomplete_tasks(self,request,queryset):
        queryset.update(status=False)
    