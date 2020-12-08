from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, UserManager

class Role(models.Model):  
  name = models.CharField(max_length=200) 

  class Meta:
    db_table = "role"

class User(models.Model):
  dni = models.CharField(max_length=8, unique=True)    
  username = models.CharField(max_length=200)    
  password = models.CharField(max_length=200, null=False)
  role = models.ForeignKey(Role, on_delete=models.PROTECT)

  class Meta:
    db_table = "user"

class UserType(AbstractBaseUser):
    dni = models.CharField(max_length=8, unique=True)
    username = models.CharField(max_length=200)
    role = models.ForeignKey(Role, on_delete=models.PROTECT)

    USERNAME_FIELD = 'dni'
    REQUIRED_FIELDS = ['']

    objects = UserManager()

    def __str__(self):
        return self.dni

    def get_role(self):
        return self.role