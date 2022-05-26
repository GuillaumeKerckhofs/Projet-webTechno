from django.shortcuts import  render, redirect
from users.forms import NewUserForm,UserLoginForm,customUserChangeForm,createTeamForm
from django.urls import reverse_lazy,reverse
from django.views.generic.edit import CreateView
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from users.models import Membership,Team

def getTeam(team_id):
	try:
		team=Team.objects.get(id=team_id)
	except:
		team=None
	return team

def getAllTeam(user):
	membership=Membership.objects.all()
	team=Team.objects.all()
	waiting_team=[]
	user_team=[]
	other_team=[]

	for t in team:
		try:
			membership=Membership.objects.get(member=user,team=t)
			if membership:
				if membership.role==4:
					waiting_team.append(t)
				else:
					user_team.append(membership)
		except:	
			other_team.append(t)
	return user_team,waiting_team,other_team

def getRelation(user,team):
	try:
		membership=Membership.objects.get(member=user,team=team)
	except:
		membership=None
	return membership

def getMembership(id):
	try:
		membership=Membership.objects.get(id=id)
	except:
		membership=None
	return membership



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


@login_required
def logout_request(request):
	logout(request)
	return redirect(homeView)

@login_required
def profil_view(request):
	user_team,waiting_team,other_team=getAllTeam(request.user)
	context = {'user_team': user_team,'waiting_team':waiting_team,'other_team':other_team}

	return render(request,'gui/HTML/profil.html',context)

@login_required
def createTeam_request(request):
	if request.method == 'POST':
		form = createTeamForm(request.POST)

		if form.is_valid():
			teamForm=form.save()
			membership=Membership.objects.create(member=request.user,team=teamForm,role=Membership.OWNER)
			return redirect(profil_view)
	else:
		form = createTeamForm()
	return render(request,template_name='gui/HTML/createTeam.html',context={'createTeam_form':form})

@login_required
def teamProfil_view(request,team_id):
	team=getTeam(team_id)
	if(team is not None):
		membership=Membership.objects.filter(team=team)
		m=getRelation(request.user,team)
		if(m is not None):
			role=m.role
			context={'team': team,'membership':membership,'role':role}
			return render(request,'gui/HTML/teamProfil.html',context)
		else:
			role=5
			context={'team': team,'membership':membership,'role':role}
			return render(request,'gui/HTML/teamProfil.html',context)

	else:
		return render(request, 'gui/HTML/teamProfil.html', {'error': 'Equipe pas trouvée.'})

@login_required
def joinTeam(request,team_id):
	team=getTeam(team_id)
	if(team is not None):
		membership = getRelation(request.user,team)
		if(membership is not None):
			return redirect(profil_view)
		else:
			membership = Membership.objects.create(member=request.user,team=team)
			return redirect(profil_view)
	else:
		return render(request, 'gui/HTML/teamProfil.html', {'error': 'Equipe pas trouvée.'})


@login_required
def updateTeam(request,membership_id,role):
	membership = getMembership(membership_id)
	if(membership is not None):
		team=membership.team
		adminMembership = getRelation(request.user,team)
		if(adminMembership is not None and adminMembership.role < 2 and adminMembership.role < membership.role):
			if(role!=0):
				membership.role=role
				membership.save()
				return redirect(teamProfil_view,team_id=team.id)
			else:
				membership.delete()
				return redirect(teamProfil_view,team_id=team.id)
		elif(role==0):
			membership.delete()
			return redirect(profil_view)
	else:
		return redirect(profil_view)
