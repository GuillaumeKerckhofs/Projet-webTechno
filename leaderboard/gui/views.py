from django.shortcuts import  render, redirect
from users.forms import NewUserForm,UserLoginForm,customUserChangeForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings

def anonymous_required(function=None, redirect_url=None):

   if not redirect_url:
       redirect_url = settings.LOGIN_REDIRECT_URL

   actual_decorator = user_passes_test(
       lambda u: u.is_anonymous,
       login_url=redirect_url
   )

   if function:
       return actual_decorator(function)
   return actual_decorator

# Create your views here.
def homeView(request):
    return render(request,'gui/HTML/home.html')


@anonymous_required
def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			return redirect(homeView)
		messages.error(request, "Unsuccessful registration. Invalid information.")
	else:
		form = NewUserForm()
	return render(request=request, template_name='gui/HTML/register.html', context={"register_form":form})


@anonymous_required
def login_request(request):
	if request.method == "POST":
		form= UserLoginForm(request.POST,request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				if user.is_active:
					login(request, user)
					return redirect(homeView)
		else:
			print(form.errors)


	else:
		form=UserLoginForm()
	return render(request=request, template_name='gui/HTML/login.html', context={"login_form":form})


@login_required
def edit_profile(request):
	if request.method == 'POST':
		form = customUserChangeForm(request.POST, instance=request.user)

		if form.is_valid():
			form.save()
			return redirect(profil_view)
	else:
		form = customUserChangeForm(instance=request.user)
	return render(request,template_name='gui/HTML/edit.html',context={'edit_form':form})


def logout_request(request):
	logout(request)
	return redirect(homeView)

@login_required
def profil_view(request):
	return render(request,'gui/HTML/profil.html')

def teamProfil_view(request):
	return render(request,'gui/HTML/TeamProfil.html')