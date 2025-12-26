from django.test import TestCase
from accounts.models import User
from .models import Task
from django.urls import reverse
from .forms import TaskForm

# Create your tests here.
class TaskModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(phone='09125094175',password='1234')
    
    def test_create_task(self):
        task = Task.objects.create(user=self.user,title='Text for test')
    
        self.assertEqual(task.title,'Text for test')
        self.assertFalse(task.status)

class ViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(phone='09125094175',password='1234')
        self.client.login(phone='09125094175',password='1234')

    def test_task_list_view(self):
        response = self.client.get(reverse('tasks'))

        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'tasks.html')
    
    def test_create_task(self):
        response = self.client.post(reverse('tasks'),{'title':'buy apples'})

        self.assertEqual(response.status_code,302)
        self.assertEqual(Task.objects.count(),1)
        self.assertEqual(Task.objects.first().title,'buy apples')

class TaskFormTest(TestCase):

    def test_valid_form(self):
        form = TaskForm(data={'title':'عنوان فرم'})
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form = TaskForm(data={'title':''})
        self.assertFalse(form.is_valid())

def test_user_cannot_see_other_tasks(self):
    user2 = User.objects.create_user(
        username='reza',
        password='1234'
    )

    Task.objects.create(
        user=user2,
        title='کار مخفی'
    )

    response = self.client.get(reverse('task_list'))

    self.assertNotContains(response, 'کار مخفی')