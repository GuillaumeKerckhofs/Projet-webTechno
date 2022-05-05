from django.shortcuts import  render, redirect
from users.forms import NewUserForm,UserLoginForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,authenticate,logout

# Create your views here.
def homeView(request):
    return render(request,'gui/HTML/Home.html')

def register_view(CreateView):
	form_class=NewUserForm
	succes_url=reverse_lazy(homeView)
	template_name='gui/HTML/register.html'

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


def login_request(request):
	if request.method == "POST":
		form= AuthenticationForm(request=request, data=request.POST)
		if form.is_valid():
			user_name = form.cleaned_data.get('user_name')
			password = form.cleaned_data.get('password')
			user = authenticate(user_name=user_name, password=password)
			if user:
				if user.is_active:
					print("login réussi")
					login(request, user)
					return redirect(homeView)
				else:
					print("compte inactif")
			else:
				print("login raté")


	else:
		form=AuthenticationForm()
	return render(request=request, template_name='gui/HTML/login.html', context={"login_form":form})


def logout_request(request):
	logout(request)
	return redirect(homeView)