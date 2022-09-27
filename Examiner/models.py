from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date
from multiselectfield import MultiSelectField

class CustomUser(AbstractUser):
    user_type_data = ((1, "EAD"), (2, "Staff"), (3, "Examiner"))
    user_type = models.CharField(default=1, choices=user_type_data, max_length=10)

class Country(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class City(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class Person(models.Model):
    name = models.CharField(max_length=124)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name


class Province(models.Model):
    name=models.CharField(max_length=50)
    def __str__(self):
       return self.name
    
class District(models.Model):
    province=models.ForeignKey(Province, on_delete=models.CASCADE)
    name=models.CharField(max_length=50)
    def __str__(self):
       return self.name



class Position(models.Model):
    name=models.CharField(max_length=20,null=True)
    objects = models.Manager()

class Subject(models.Model):
    subjectCode=models.CharField(max_length=5,null=True)
    subjectName=models.CharField(max_length=20,null=True)
    datecreated= models.DateField(auto_now=True)
    dateupdated= models.DateField(auto_now=True)

    def __str__(self):
       return self.subjectCode

class Invitation(models.Model):
    #toAddress=models.ForeignKey(CustomUser, on_delete = models.CASCADE,null=True,blank=True)
    toAddress=models.ManyToManyField(CustomUser)
    title=models.CharField(max_length=50,null=True)
    datecreated= models.DateField(auto_now=True)
    dateupdated= models.DateField(auto_now=True)
    #message=models.TextField(max_length=500,null=True)
    StatusConfirm=models.IntegerField(default=0)
    objects = models.Manager()


class EAD(models.Model):
    user = models.OneToOneField(CustomUser, on_delete = models.CASCADE,null=True,blank=True)
    firstName=models.CharField(max_length=50,null=True)
    LastName=models.CharField(max_length=50,null=True)
    UserName=models.CharField(max_length=50,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def save(self,*args,**kwargs):
            super().save(*args,**kwargs)
            if not self.user:
                self.user= CustomUser.objects.create_user(username=self.UserName,
                                                         first_name=self.firstName,last_name=self.LastName,
                                                         password='password3', email='MicroVich.1@abc.com',
                                                         is_staff=True,
                                                         user_type=1
                                                        )
                self.save()

    objects = models.Manager()


class Examiner(models.Model):
    user=models.OneToOneField(CustomUser,
        on_delete=models.CASCADE,null=True,blank=True)
    subject=models.ForeignKey(Subject, on_delete=models.CASCADE,null=True)
    position=models.ForeignKey(Position,on_delete=models.CASCADE,null=True)
    name=models.CharField(max_length=50,null=True)
    ExaminerCode=models.CharField(max_length=50,null=True,unique=True)
    Address=models.CharField(max_length=500,null=True)
    district=models.ForeignKey(District, on_delete=models.CASCADE,null=True)
    province=models.ForeignKey(Province, on_delete=models.CASCADE,null=True)
    AccountDetails=models.CharField(max_length=150,null=True)
    NRC=models.CharField(max_length=12,null=True)
    TPIN=models.CharField(max_length=10,null=True)
    cell_Number=models.CharField(max_length=12,null=True)
    email=models.EmailField(null=True)
    country=models.ForeignKey(Country, on_delete=models.SET_NULL,null=True)
    city=models.ForeignKey(City, on_delete=models.SET_NULL,null=True)

    #participating=models.BooleanField(default=False)
    """ 
    @property
    def code(self):
        return "ECZ%03d%s"% (self.id,self.subject)
    """
    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
        if not self.ExaminerCode:
            td=str(date.today().year)
            self.ExaminerCode=td[-2:]+'-'+self.subject.subjectCode+str(self.id)
            self.user=CustomUser.objects.create_user(username=self.ExaminerCode,
                            password='password3', email='MicroVich.1@abc.com',
                            user_type=3
                            )
            self.save()
    objects = models.Manager()


#==============================


