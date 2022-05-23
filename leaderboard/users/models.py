from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from datetime import datetime  


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, user_name, first_name, last_name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_dev', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, user_name, first_name, last_name, password, **other_fields)

    def create_user(self, email, user_name, first_name, last_name, password, **other_fields):

        other_fields.setdefault('is_active', True)

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name,
                          first_name=first_name, last_name=last_name, **other_fields)
        user.set_password(password)
        user.save()
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):

    user_name = models.CharField(max_length=150, unique=True)
    email = models.EmailField( unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    is_dev = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True,editable=False)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = ['email', 'first_name','last_name']

    def __str__(self):
        return self.user_name

class Team(models.Model):
    name=models.CharField(max_length=150, unique=True)
    members=models.ManyToManyField(CustomUser,through="Membership")

    def __str__(self):
        return self.name

class Membership(models.Model):

    OWNER = 1
    ADMIN = 2
    MEMBER = 3
    PENDING = 4
      
    ROLE_CHOICES = (
        (OWNER, 'Propriétaire'),
        (ADMIN, 'Admin'),
        (MEMBER, 'Membre'),
        (PENDING,'En attente')
    )

    member = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    date_joined = models.DateField(default=datetime.now, blank=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=PENDING)

    def getRole(self):
        if(self.role==1):
            return 'Propriétaire'
        elif(self.role==2):
            return 'Admin'
        elif(self.role==3):
            return 'Membre'
        else:
            return 'En attente'