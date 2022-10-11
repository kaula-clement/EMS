from email.policy import default
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date
from multiselectfield import MultiSelectField

class CustomUser(AbstractUser):
    user_type_data = ((1, "EAD"), (2, "Staff"), (3, "Examiner"))
    user_type = models.IntegerField(default=1, choices=user_type_data)

class Country(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class City(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


    
    
class Bank(models.Model):
    name=models.CharField(max_length=64)
    def __str__(self):
        return self.name
    
    
class BankBranch(models.Model):
    bank=models.ForeignKey(Bank,on_delete=models.CASCADE,null=True)
    name=models.CharField(max_length=64)
    sortcode=models.IntegerField()
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
    def __str__(self):
       return self.name

class Subject(models.Model):
    subjectCode=models.CharField(max_length=5,null=True)
    subjectName=models.CharField(max_length=20,null=True)
    subjectDescription=models.CharField(max_length=50,null=True,blank=True)
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
    user = models.OneToOneField(CustomUser, on_delete = models.SET_NULL,null=True,blank=True)
    firstName=models.CharField(max_length=50,null=True)
    LastName=models.CharField(max_length=50,null=True)
    UserName=models.CharField(max_length=50,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    address=models.CharField(max_length=50,null=True,blank=True)
    province=models.ForeignKey(Province, on_delete=models.SET_NULL,null=True,blank=True)
    district=models.ForeignKey(District, on_delete=models.SET_NULL,null=True,blank=True)
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
    subject=models.ForeignKey(Subject, on_delete=models.SET_NULL,null=True)
    position=models.ForeignKey(Position,on_delete=models.SET_NULL,null=True)
    name=models.CharField(max_length=50,null=True)
    ExaminerCode=models.CharField(max_length=50,null=True,unique=True)
    Address=models.CharField(max_length=500,null=True)
    district=models.ForeignKey(District, on_delete=models.SET_NULL,null=True)
    province=models.ForeignKey(Province, on_delete=models.SET_NULL,null=True)
    bank=models.ForeignKey(Bank,on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(BankBranch,on_delete=models.SET_NULL,null=True,blank=True)
    AccountDetails=models.CharField(max_length=150,null=True)
    NRC=models.CharField(max_length=12,null=True)
    TPIN=models.CharField(max_length=10,null=True)
    cell_Number=models.CharField(max_length=12,null=True)
    email=models.EmailField(null=True)
    country=models.ForeignKey(Country, on_delete=models.SET_NULL,null=True)
    city=models.ForeignKey(City, on_delete=models.SET_NULL,null=True)
    availability=models.BooleanField(default=False)

    objects = models.Manager()


class Staff(models.Model):
    user=models.OneToOneField(CustomUser,
        on_delete=models.CASCADE,null=True,blank=True)
    name=models.CharField(max_length=64)
    Username=models.CharField( max_length=50)
    def save(self,*args,**kwargs):
            super().save(*args,**kwargs)
            if not self.user:
                self.user= CustomUser.objects.create_user(username=self.Username,
                                                         first_name=self.name,
                                                         password='password3', email='MicroVich.1@abc.com',
                                                         is_staff=True,
                                                         user_type=2
                                                        )
                self.save()

#==============================


class districtcsv(models.Model):
    code=models.IntegerField()
    name=models.CharField(max_length=50)
    
class subjectselector(models.Model):
    code=models.CharField(max_length=50)
    papernumber=models.IntegerField()
    
from django.dispatch import receiver

@receiver(models.signals.post_delete, sender=Examiner)
def handle_deleted_examiner(sender, instance, **kwargs):
    if instance.user:
        instance.user.delete()
        
@receiver(models.signals.post_delete, sender=Staff)
def handle_deleted_staff(sender, instance, **kwargs):
    if instance.user:
        instance.user.delete()
        
@receiver(models.signals.post_delete, sender=EAD)
def handle_deleted_ead(sender, instance, **kwargs):
    if instance.user:
        instance.user.delete()
   