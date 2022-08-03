from django import forms
from django.db import models
from .models import Category,Link,Boards,submittedModel
from django.forms import ModelForm,Form
from django.db import models
from users.models import Membership,Team

class BoardForm(ModelForm):
    class Meta:
        model=Boards
        fields=("name","description","closingDate","category")
        labels= {
            "name": "Nom du leaderboard",
            "description": "description",
            "closingDate": "Date de fin",
            "category": "Catégorie",
        }

        widgets = {
            'category' : forms.Select()
        }

class updateBoardForm(ModelForm):
    class Meta:
        model=Boards
        fields=("name","description","closingDate")
        labels= {
            "name": "Nom du leaderboard",
            "description": "description",
            "closingDate": "Date de fin",
        }

class SubmissionForm(Form):
    team=forms.ModelChoiceField(queryset=Membership.objects.all())
    file=forms.FileField(label="Votre modèle")
    class Meta:
        fields = ("team","file")

    def __init__(self, *args, **kwargs):
        current_user = kwargs.pop('current_user', None)
        super(SubmissionForm, self).__init__(*args, **kwargs)
        self.fields['team']=forms.ModelChoiceField(queryset=Membership.objects.filter(member=current_user,role__lt=4))