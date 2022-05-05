from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm,AuthenticationForm
from .models import CustomUser


# Create your forms here.

class NewUserForm(UserCreationForm):

	class Meta:
		model = CustomUser
		fields = ("user_name", "email","first_name","last_name", "password1", "password2",'is_active', 'is_staff',"is_dev")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)

		if commit:
			user.save()
		return user

class UserLoginForm(AuthenticationForm):
	class Meta:
		model = CustomUser
		fields = ('username', 'password')

	#user_name=forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Pseudo'}))
	#password=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'mot de passe'}))
	#fields=("user_name","password")

	#class Meta:
	#	model = CustomUser
	#	fields=("user_name","password")

	#	def clean(self):
	#		if self.is_valid():
	#			user_name=self.cleaned_data('user_name')
	#			password=self.cleaned_data('password')
	#			if not authenticate(user_name=user_name,password=password):
	#				raise forms.ValidationError("Invalid LOGIN")