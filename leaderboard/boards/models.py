from django.db import models
from datetime import datetime  
from users.models import Team,CustomUser
from django.conf import settings

# Create your models here.

class Link(models.Model):
    name=models.CharField(max_length=150,unique=True)
    #path= models.FilePathField(path=str(settings.DATASET_FILES_DIRS[0]), recursive=True, max_length=100, allow_folders=True)
    path= models.FilePathField(path="public/dataset", recursive=True, max_length=100, allow_folders=True)

    def __str__(self):
        return '%s' % self.name

class Category(models.Model):
    name=models.CharField(max_length=150,unique=True)
    #path= models.FilePathField(path=str(settings.TEST_FILES_DIRS[0]), recursive=False, max_length=100)
    path= models.FilePathField(path="public/python", recursive=False, max_length=100)
    link_to_dataset=models.ForeignKey(Link, on_delete=models.CASCADE)

    LOCALISATION = 1
    CLASSIFICATION = 2
      
    CATEGORY_CHOICES = (
        (LOCALISATION, 'Localisation'),
        (CLASSIFICATION, 'Classification'),
    )

    category = models.PositiveSmallIntegerField(choices=CATEGORY_CHOICES, default=LOCALISATION)

    def __str__(self):
        return '%s' % self.name

    def getCategory(self):
        if(self.category==1):
            return 'Localisation'
        elif(self.category==2):
            return 'Classification'


class Boards(models.Model):
    name=models.CharField(max_length=150,unique=True)
    description = models.TextField(blank=True)
    createdAt = models.DateField(default=datetime.now, blank=True)
    closingDate = models.DateField(blank=True)
    category=models.ForeignKey(Category, on_delete=models.CASCADE)


class submittedModel(models.Model):
    best_model=models.CharField(max_length=150)
    number_entries = models.IntegerField(default=1,blank=True)
    score = models.FloatField(default=None,blank=True)
    last_score = models.FloatField(default=None,blank=True)
    date_published = models.DateField(default=datetime.now, blank=True)
    team=models.ForeignKey(Team, on_delete=models.CASCADE)
    board=models.ForeignKey(Boards,on_delete=models.CASCADE,default=None)
    
    def __str__(self):
        return self.best_model
