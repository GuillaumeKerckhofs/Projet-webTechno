from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm,AuthenticationForm
from .models import CustomUser,Team,Membership
from django.forms import ModelForm
from django.db import models


# Create your forms here.

class NewUserForm(UserCreationForm):

	class Meta:
		model = CustomUser
		fields = ("user_name", "email","first_name","last_name", "password1", "password2", 'is_staff',"is_dev")

		labels = {
            'user_name': 'Pseudo',
			'email': 'Email',
			'first_name': 'Prénom',
			'last_name': 'Nom',
			'is_dev': 'Etes-vous un développeur ?',
        }

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)

		if commit:
			user.save()
		return user

class UserLoginForm(AuthenticationForm):
	class Meta:
		model = CustomUser
		fields = ('user_name', 'password')
		labels = {
            'user_name': 'Pseudo',
        }

class customUserChangeForm(UserChangeForm):
	class Meta:
		model = CustomUser
		fields = ("email","first_name","last_name","is_dev")
		labels = {
			'email': 'Email',
			'first_name': 'Prénom',
			'last_name': 'Nom',
			'is_dev': 'Etes-vous un développeur ?',
        }

class teamForm(ModelForm):

	class Meta:
		model=Team
		fields=["name"]
		labels={
			'name': 'Nom de l\'équipe',
		}

class updateUserRoleForm(ModelForm):


	class Meta:
		model= Membership
		fields =("role",)
		labels={
			'role': 'Nouveau role',
		}

	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user', None)
		super(updateUserRoleForm, self).__init__(*args, **kwargs)
		limited_choices = [(Membership.ADMIN, 'Admin'),(Membership.MEMBER, 'Membre')]
		self.fields['role'] = forms.ChoiceField(choices=limited_choices)
