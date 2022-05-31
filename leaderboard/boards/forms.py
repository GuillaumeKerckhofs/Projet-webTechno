from django import forms
from .models import Category,Link,Boards,submittedModel
from django.forms import ModelForm
from django.db import models

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