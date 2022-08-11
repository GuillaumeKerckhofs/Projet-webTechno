from django import forms
from django.db import models
from .models import Category,Link,Boards,submittedModel
from django.forms import ModelForm,Form
from django.db import models
from users.models import Membership,Team
from django.core.exceptions import ValidationError

def validate_file_extension(value):
  import os
  ext = os.path.splitext(value.name)[1]
  valid_extensions = ['.h5','.pt','.pth']
  if not ext in valid_extensions:
    raise ValidationError(u'Fichier pas supporté!')




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
    file=forms.FileField(label="Votre modèle", validators=[validate_file_extension])
    entrySize=forms.IntegerField(label="Taille de l'entrée",help_text="Example: 224 pour VGG16")
    class Meta:
        fields = ("team","file","entrySize")

    def __init__(self, *args, **kwargs):
        current_user = kwargs.pop('current_user', None)
        super(SubmissionForm, self).__init__(*args, **kwargs)
        self.fields['team']=forms.ModelChoiceField(queryset=Membership.objects.filter(member=current_user,role__lt=4))