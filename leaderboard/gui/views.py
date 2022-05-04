from django.shortcuts import  render, redirect
from users.forms import NewUserForm
from django.contrib.auth import login
from django.contrib import messages

# Create your views here.
def homeView(request):
    return render(request,'gui/HTML/Home.html')

def register(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Inscription réussi." )
			return redirect("/home")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render(request=request, template_name='gui/HTML/register.html', context={"register_form":form})
