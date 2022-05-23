from django.shortcuts import  render, redirect
from users.forms import NewUserForm,UserLoginForm,customUserChangeForm,createTeamForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from users.models import Membership,Team

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
	context={}
	if request.user.is_authenticated:
		membership=Membership.objects.filter(member=request.user)
		context={'membership': membership}
	return render(request,'gui/HTML/home.html',context)


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
	membership=Membership.objects.filter(member=request.user)
	if request.method == 'POST':
		form = customUserChangeForm(request.POST, instance=request.user)

		if form.is_valid():
			form.save()
			return redirect(profil_view)
	else:
		form = customUserChangeForm(instance=request.user)
	return render(request,template_name='gui/HTML/edit.html',context={'edit_form':form,'membership': membership})


@login_required
def logout_request(request):
	logout(request)
	return redirect(homeView)

@login_required
def profil_view(request):
	membership=Membership.objects.filter(member=request.user)
	context = {'membership': membership}
	return render(request,'gui/HTML/profil.html',context)

@login_required
def createTeam_request(request):
	membership=Membership.objects.filter(member=request.user)
	if request.method == 'POST':
		form = createTeamForm(request.POST)

		if form.is_valid():
			teamForm=form.save()
			membership=Membership.objects.create(member=request.user,team=teamForm,role=Membership.OWNER)
			return redirect(profil_view)
	else:
		form = createTeamForm()
	return render(request,template_name='gui/HTML/createTeam.html',context={'createTeam_form':form,'membership': membership})


def teamProfil_view(request):
	team=Team.objects.all()
	waiting_team=[]
	if request.user.is_authenticated:
		new_team=[]
		for t in team:
			try:
				membership=Membership.objects.get(member=request.user,team=t)
				if membership:
					if membership.role==4:
						waiting_team.append(t)
			except:	
				new_team.append(t)
		team=new_team
		
	context={'team': team,'waiting_team':waiting_team}
	return render(request,'gui/HTML/TeamProfil.html',context)