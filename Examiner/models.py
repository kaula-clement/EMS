from email.policy import default
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date
from auditlog.registry import auditlog


class CustomUser(AbstractUser):
    user_type_data = ((0, "ADMIN"),(1, "EAD"), (2, "FAD"), (3, "Examiner"),(4,"Station-Admin"))
    user_type = models.IntegerField(default=1, choices=user_type_data)
    is_admin=models.BooleanField(default=False)
    #email= models.EmailField(unique=True)

    
    
class Bank(models.Model):
    name=models.CharField(max_length=64)
    def __str__(self):
        return self.name
    
    
class BankBranch(models.Model):
    bank=models.ForeignKey(Bank,on_delete=models.CASCADE,null=True)
    name=models.CharField(max_length=64)
    sortcode=models.CharField(max_length=6)
    def __str__(self):
        return self.name


class Province(models.Model):
    name=models.CharField(max_length=50)
    def __str__(self):
       return self.name
    
class District(models.Model):
    province=models.ForeignKey(Province, on_delete=models.SET_NULL, blank=True, null=True)
    code=models.IntegerField(unique=True)
    name=models.CharField(max_length=50)
    def __str__(self):
       return self.name
   
class Station(models.Model):
    province=models.ForeignKey(Province,on_delete=models.SET_NULL, blank=True, null=True)
    name=models.CharField(max_length=50,unique=True)
    def __str__(self):
       return self.name

class Session(models.Model):
    name=models.CharField(max_length=20)
    start_date=models.DateField()
    end_date=models.DateField()
    active=models.BooleanField(default=True)
    def __str__(self):
       return self.name


class Position(models.Model):
    name=models.CharField(max_length=50,null=True)
    def __str__(self):
       return self.name
 
regions=(('LUSAKA','LUSAKA'),('COPPERBELT','COPPERBELT'),('MONZE','MONZE'),
             ('KAPIRI','KAPIRI'),('LIVINGSTONE','LIVINGSTONE'),
                ('CHOMA','CHOMA'),('MWANDI','MWANDI'),('LUNTE','LUNTE'),('MWENSE','MWENSE'),
                ('KASENENGWA','KASENENGWA'),('CHISAMBA','CHISAMBA'),('CHIBOMBO','CHIBOMBO')) 
   
class Subject(models.Model):
    subjectCode=models.CharField(max_length=5,unique=True)
    subjectName=models.CharField(max_length=20,null=True)
    subjectDescription=models.CharField(max_length=50,null=True,blank=True)
    datecreated= models.DateField(auto_now=True)
    dateupdated= models.DateField(auto_now=True) 

    def __str__(self):
       return self.subjectName

class Paper(models.Model):
    subject=models.ForeignKey(Subject,to_field="subjectCode",on_delete=models.CASCADE)
    paper_number=models.IntegerField(default=0)
    paper_name=models.CharField(max_length=7)
    paper_description=models.CharField(max_length=50)
    
    def __str__(self):
        return self.paper_name

class MarkingVenue(models.Model):
    paper=models.ForeignKey(Paper,on_delete=models.CASCADE)
    center=models.CharField(max_length=50,choices=regions,null=True,blank=True)
    
   
    


class EAD(models.Model):
    user = models.OneToOneField(CustomUser, on_delete = models.CASCADE,null=True,blank=True)
    first_name=models.CharField(max_length=50,null=True)
    last_name=models.CharField(max_length=50,null=True)
    username=models.CharField(max_length=50,null=True)
    email=models.EmailField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def save(self,*args,**kwargs):
            super().save(*args,**kwargs)
            if not self.user:
                self.user= CustomUser.objects.create_user(username=self.username,
                                                         first_name=self.first_name,
                                                         last_name=self.last_name,
                                                         password='password3', email=self.email,
                                                         is_staff=True,
                                                         user_type=1
                                                        )
                self.save()

    objects = models.Manager()
    def __str__(self):
        return self.username



class Examiner(models.Model):
    user=models.OneToOneField(CustomUser,
        on_delete=models.CASCADE,null=True,blank=True)
    gender_data = ((0,"SELECT GENDER"),(1, "MALE"), (2, "FEMALE"))
    gender = models.IntegerField(default=0, choices=gender_data)
    subject=models.ForeignKey(Subject,to_field="subjectCode",db_column="Subject_Code", on_delete=models.SET_NULL,null=True,blank=True)
    paper=models.ForeignKey(Paper,db_column="Paper_Number", on_delete=models.SET_NULL,null=True)
    position=models.ForeignKey(Position,on_delete=models.SET_NULL,null=True)
    #middle_name=models.CharField(max_length=50,null=True,blank=True)
    first_name=models.CharField(max_length=50,null=True) 
    last_name=models.CharField(max_length=50,null=True)
    ExaminerCode=models.CharField(max_length=11,unique=True)
    Address=models.CharField(max_length=500,null=True)
    province=models.ForeignKey(Province, on_delete=models.SET_NULL,null=True) 
    district=models.ForeignKey(Station,related_name="district", on_delete=models.SET_NULL,blank=True,null=True)#from station 
    to_province =models.CharField(max_length=50,choices=regions,null=True,blank=True)   
    bank=models.ForeignKey(Bank,on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(BankBranch,on_delete=models.SET_NULL,null=True,blank=True)
    AccountDetails=models.CharField(max_length=150,null=True)
    #payment=models.ForeignKey("Payment", verbose_name=("payment"), on_delete=models.SET_NULL,null=True,blank=True)
    nrc_regex=RegexValidator(regex=r'([0-9]{6})\/([0-9]{2})\/([0-9]{1})', message="Enter a valid NRC Number")
    NRC=models.CharField(max_length=11,null=True,validators=[nrc_regex])
    
    t_pin_regex=RegexValidator(regex=r'([0-9]{10})', message="Enter a valid T-Pin Number [0~9 10 digits]")
    TPIN=models.CharField(max_length=10,null=True,validators=[t_pin_regex])
    
    phone_regex=RegexValidator(regex=r'0([1-9]{9})', message="Enter a valid Phone Number starting: 0")
    cell_Number=models.CharField(max_length=10,null=True,validators=[phone_regex])
    
    email=models.EmailField(null=True,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved=models.BooleanField(default=False)
    availability=models.BooleanField(default=False) 
    session=models.ForeignKey(Session,on_delete=models.CASCADE,null=True,blank=True)
    mail_count=models.IntegerField(default=0)
    objects = models.Manager()
    def __str__(self):
        return self.first_name +' '+ self.last_name
    def save(self, force_insert=False, force_update=False):
        self.first_name= self.first_name.upper()
        self.last_name= self.last_name.upper()
        super(Examiner, self).save(force_insert, force_update)
        
      
class ECZStaff(models.Model):
    user=models.OneToOneField(CustomUser,
        on_delete=models.CASCADE,null=True,blank=True)
    username=models.CharField(max_length=50)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    email=models.EmailField(unique=True)
    #subject=models.ForeignKey(Subject,to_field="subjectCode",db_column="Subject_Code", on_delete=models.SET_NULL,null=True,blank=True)
    #paper =models.ForeignKey(Paper,on_delete=models.SET_NULL,null=True,blank=True)
    center=models.CharField(max_length=50,choices=regions,null=True,blank=True)
    def save(self,*args,**kwargs):
            super().save(*args,**kwargs)
            if not self.user:
                self.user= CustomUser.objects.create_user(username=self.username,
                                                         first_name=self.first_name,
                                                         last_name=self.last_name,
                                                         password='password3', email=self.email,
                                                         is_staff=True,
                                                         user_type=4
                                                        )
                self.save()
    def __str__(self):
        return self.username

class Invitation(models.Model):
    fromAddress=models.ForeignKey(EAD, on_delete = models.CASCADE,null=True,blank=True)
    toAddress=models.ForeignKey(Examiner, on_delete = models.CASCADE,null=True,blank=True)
    title=models.CharField(max_length=50,null=True)
    datecreated= models.DateField(auto_now=True)
    dateupdated= models.DateField(auto_now=True)
    msg=models.TextField(max_length=500,null=True)
    StatusConfirm=models.IntegerField(default=0)
    objects = models.Manager()


class Staff(models.Model):
    user=models.OneToOneField(CustomUser,
        on_delete=models.CASCADE,null=True,blank=True)
    first_name=models.CharField(max_length=50,null=True)    
    last_name=models.CharField(max_length=50,null=True)
    username=models.CharField(max_length=50,null=True)
    email=models.EmailField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def save(self,*args,**kwargs):
            super().save(*args,**kwargs)
            if not self.user:
                self.user= CustomUser.objects.create_user(username=self.username,
                                                         first_name=self.first_name,
                                                         last_name=self.last_name,
                                                         password='password3', email=self.email,
                                                         is_staff=True,
                                                         user_type=2
                                                        )
                self.save()

#==============================


class districtcsv(models.Model):
    code=models.IntegerField()
    name=models.CharField(max_length=50)
    

   
class comment(models.Model):
    commentAuthor=models.ForeignKey(CustomUser,on_delete=models.DO_NOTHING)
    examiner=models.ForeignKey(Examiner,on_delete=models.CASCADE)
    title=models.CharField(max_length=50)
    msg=models.TextField(max_length=255)
    msg2=models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class SchedulePay(models.Model):
    FromDistrict=models.ForeignKey(Station,to_field="name",db_column="station",on_delete=models.SET_NULL,null=True,blank=True)
    LUSAKA=models.IntegerField()
    COPPERBELT=models.IntegerField()
    MONZE=models.IntegerField()
    KAPIRI=models.IntegerField()
    LIVINGSTONE=models.IntegerField()
    CHOMA=models.IntegerField()
    MWANDI=models.IntegerField()
    LUNTE=models.IntegerField()
    MWENSE=models.IntegerField()
    KASENENGWA=models.IntegerField()
    CHISAMBA=models.IntegerField()
    CHIBOMBO=models.IntegerField()
    
class Payment(models.Model):
    examiner=models.ForeignKey(Examiner, on_delete=models.CASCADE)
    transport=models.FloatField(default=0.00)
    daily_allowance=models.FloatField(default=0.00)
    
class Attendance(models.Model):
    examiner=models.ForeignKey(Examiner,on_delete=models.CASCADE, related_name="attendance_examiner")
    status=models.IntegerField(default=1)
    


    
from django.dispatch import receiver

@receiver(models.signals.post_delete, sender=Examiner)
def handle_deleted_examiner(sender, instance, **kwargs):
    if instance.user:
        instance.user.delete()



auditlog.register(CustomUser)
auditlog.register(Bank)
auditlog.register(BankBranch)
auditlog.register(Province)
auditlog.register(District)
auditlog.register(Station)
auditlog.register(Session)
auditlog.register(Position)
auditlog.register(Subject)
auditlog.register(Paper)
auditlog.register(Examiner)
auditlog.register(ECZStaff)
auditlog.register(Staff)
auditlog.register(SchedulePay)
auditlog.register(Payment)
auditlog.register(Attendance)