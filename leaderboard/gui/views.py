from django.shortcuts import  render, redirect
from users.forms import NewUserForm,UserLoginForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,authenticate,logout

# Create your views here.
def homeView(request):
    return render(request,'gui/HTML/homeTest.html')

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
		form= UserLoginForm(request.POST,request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				if user.is_active:
					print("login réussi")
					login(request, user)
					return redirect(homeView)
				else:
					print("compte inactif")
			else:
				print("login raté")
		else:
			print(form.errors)


	else:
		form=UserLoginForm()
	return render(request=request, template_name='gui/HTML/login.html', context={"login_form":form})


def logout_request(request):
	logout(request)
	return redirect(homeView)

def profil_view(request):
	return render(request,'gui/HTML/profil.html')

def teamProfil_view(request):
	return render(request,'gui/HTML/TeamProfil.html')