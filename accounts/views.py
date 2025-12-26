from django.shortcuts import render,redirect,get_object_or_404
from .forms import Signup_Form
from django.contrib.auth import logout,login,authenticate
from .models import User,PasswordToken
from django.contrib import messages
from django.contrib.auth.hashers import check_password,make_password
from .utils import generate_token
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# Create your views here.
def login_form(request):
    if request.method == 'POST':
        phone = request.POST['phone-number']
        password = request.POST['password']

        user = authenticate(request,phone=phone,password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'نام کاربری یا رمز عبور اشتباه است')

    return render(request,'login.html',{})

def signup(request):
    if request.method == 'POST':
        form = Signup_Form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            messages.error(request,'نام کاربری یا رمز عبور اشتباه است.')

    form = Signup_Form()    
    return render(request,'signup.html',{'form':form})

def logout_site(request):
    logout(request)
    return redirect('home')

def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = request.user

        if not check_password(current_password,user.password):
            return render(request,'change-password.html',{'error':'رمز عبور فعلی اشتباه است.'})
        
        if new_password != confirm_password:
            return render(request,'change-password.html',{'error':'رمز عبور با تکرار آن مطابقت ندارد.'})
        
        user.password = make_password(new_password)
        user.save()

        return redirect('change_password_done')
    return render(request,'change-password.html')

def change_password_done(request):
    return render(request,'change-password-done.html')

def send_email_reset(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(request,'reset_email.html',{'error':'کاربر یافت نشد.'})
        
        token = generate_token(email)


        PasswordToken.objects.create(user=user,token=token)

        reset_link = f'http://127.0.0.1:8000/reset_password/{token}'

        html_message = render_to_string('email.html',{'reset_link':reset_link,'site_name':'ToDo List'})

        # plain_message = strip_tags(html_message)
        
        send_mail(
            subject='بازیابی رمز عبور',
            message= f'برای بازیابی رمز عبور روی لینک زیر کلیک کنید\n{reset_link}', # you can use plain_message here
            from_email= None,
            recipient_list= [email],
            html_message=html_message)
        
        return render(request,'reset_email_sent.html')
    
    return render(request,'reset_email.html')

def reset_form(request,token):
    reset_obj = get_object_or_404(PasswordToken,token=token)

    if request.method == 'POST':
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request,'رمز ها یکی نیستند❌')
            return render(request,'reset-form.html')
        
        password = make_password(password1)
        user = reset_obj.user
        user.password = password
        user.save()
        reset_obj.delete()
        return render(request,'reset_password_done.html')
    
    return render(request,'reset-form.html')