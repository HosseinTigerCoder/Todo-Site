from django.shortcuts import render,redirect,get_object_or_404
from .models import Task
from .forms import EditTaskForm,TaskForm
from django.contrib import messages
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from django.urls import reverse_lazy

# Create your views here.
class HomeView(View):
    def get(self,request):
        return render(request,'home.html',{})

class TaskListView(LoginRequiredMixin,View):
    login_url = 'login'
    
    def get(self,request):
        form = TaskForm()
        queryset = Task.objects.filter(user=request.user)
        return render(request,'tasks.html',{'tasks':queryset,'form':form})
    
    def post(self,request):
        form = TaskForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            date = form.cleaned_data['reminder_date']
            Task.objects.create(title=title,user=request.user,reminder_date=date)
            return redirect('tasks')
        queryset = Task.objects.filter(user=request.user)
        return render(request,'tasks.html',{'tasks':queryset,'form':form})

class CheckTaskView(View):
    def post(self,request,pk):
        task = get_object_or_404(Task,pk=pk)
        task.status = not task.status
        task.save()
        return redirect('tasks')
    
class EditTaskView(View):
    def get(self,request,pk):
        task = get_object_or_404(Task,pk=pk)
        form = EditTaskForm(instance=task)
        return render(request,'edit-task.html',{'form':form})
    
    def post(self,request,pk):
        task = get_object_or_404(Task,pk=pk)
        form = EditTaskForm(request.POST,instance=task)
        if form.is_valid():
            form.save()
            messages.success(self.request,'کار ویرایش شد.')
            return redirect('tasks')
        return render(request, 'edit-task.html', {'form': form})

class DeleteTaskView(View):
    def get(self,request,pk):
        Task.objects.get(pk=pk).delete()
        return redirect('tasks')
    
def about(request):
    return render(request,'contact-us.html')