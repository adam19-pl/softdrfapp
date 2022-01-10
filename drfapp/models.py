from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
STATUS = ((0, 'new'), (1, 'old'))
GENDER = ((0, 'male'), (1, 'female'))


class CustomUserManager(BaseUserManager):
    def create_superuser(self, email, firstname, lastname, password, gender=GENDER[0], age=18, phone=None,
                         **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser is_staff must be assigned to True')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser is_superuser must be assigned to True')

        return self.create_user(email, firstname, lastname, password, gender=GENDER[0], age=18, phone=None,
                                **other_fields)

    def create_user(self, email, firstname, lastname, password, gender=GENDER[0], age=18, phone=None,
                    **other_fields):

        if not email:
            raise ValueError('You must provide an email')
        if not password:
            raise ValueError('The password should not be empty')

        email = self.normalize_email(email)
        user = self.model(email=email, firstname=firstname, lastname=lastname, gender=gender, age=age, phone=phone,
                          **other_fields)
        user.set_password(password)
        user.save()
        return user


class NewUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=256, unique=True)
    firstname = models.CharField(max_length=256)
    lastname = models.CharField(max_length=256)
    gender = models.CharField(choices=GENDER, default=GENDER[0], max_length=55)
    age = models.PositiveIntegerField(null=False, blank=False, default=18)
    phone = models.CharField(null=True, blank=True, max_length=55)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstname', 'lastname']

    def __str__(self):
        return self.email


class Project(models.Model):
    owner = models.ForeignKey(NewUser, related_name='projects', on_delete=models.CASCADE, )
    title = models.CharField(blank=False, null=False, max_length=256)
    description = models.TextField(blank=False, null=False, )
    started = models.DateTimeField(default=timezone.now, null=False)
    ended = models.DateTimeField(default=None, null=True)
    status = models.CharField(choices=STATUS, default=STATUS[0], max_length=256)
    employers = models.ManyToManyField(User)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class Comment(models.Model):
    project = models.ForeignKey(Project, related_name='project', on_delete=models.CASCADE)
    autor = models.ForeignKey(NewUser, related_name='comments', on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=True, null=True, )
