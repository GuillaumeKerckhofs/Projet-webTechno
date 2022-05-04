from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
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