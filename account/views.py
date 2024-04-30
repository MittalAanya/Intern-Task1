from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from account.models import User
from django.contrib import messages

User = get_user_model() 
# Create your views here.
@login_required(login_url='login')
def home(request):
    user = request.user 
    context = {
        'user': user  
    }
    return render(request, 'account/home.html', context)

def SignupView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        profile_picture = request.FILES.get('profile_picture')
        user_type = request.POST.get('userType')

        if password1 != password2:
            return HttpResponse("Your password and confirm password are different!!")
        else:
            try:
                my_user = User.objects.create_user(
                    username=username,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    address=address,
                    city=city,
                    state=state,
                    pincode=pincode,
                    profile_picture=profile_picture
                )

                my_user.set_password(password1)
                my_user.save()
                group = Group.objects.get(name=user_type)
                group.user_set.add(my_user)
                return redirect('login')
            except Group.DoesNotExist:
                messages.error(request, 'Group does not exist. Please select a valid group.')
                return redirect('signup')

            except Exception as e:
                messages.error(request, f'An error occurred: {str(e)}')
                return redirect('signup')

    return render(request, 'account/signup.html')


def LoginView(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return HttpResponse ("Username or Password is incorrect!!!")

    return render (request,'account/login.html')

def LogoutView(request):
    logout(request)
    return redirect('login')