from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from datetime import date

# Create your models here.
class UserManager(BaseUserManager):
    
    def create_user(self,username,email,not_admin = True,password = None,brith = None,city = None,sex = None):
        ageUser = 0 
        if not username:
            raise ValueError("must have username")
        if not_admin:
            if not brith:
               raise ValueError("must have brith") 
            else:
               today = date.today()
               ageUser = today.year - brith.year - ((today.month, today.day) < (brith.month, brith.day))
            if not city:
               raise ValueError("must have city")
            if not sex:
               raise ValueError("must have sex")
       
        user = self.model(
            username = username,
            brith = brith,
            age = ageUser,
            cityLiveIn = city,
            Sex = sex)
        
    
        if email:
            user = self.model(email = self.normalize_email(email),)
        if password: 
          user.set_password(password)
        else:
            raise ValueError("must have password")
        
        user.save(using = self._db)
   
    def create_superuser(self,username,email,password):
        user = self.create_user(username = username,
        email= email,
        not_admin = False,
        password=password)

        #user.is_admin = True
        user.set_super(True)
       
        user.save(using = self._db)
        return user
        

class User(AbstractBaseUser):

    email = models.EmailField(verbose_name="email", max_length=50)
    username = models.CharField(max_length=30,unique=True)
  

    date_join = models.DateField(verbose_name="date joined", auto_now_add= True)
    is_admin = models.BooleanField(default=False)
    #is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    birth = models.DateField(verbose_name="birth",null= True)
    age = models.IntegerField(verbose_name="age",null= True)
    cityLiveIn = models.CharField(verbose_name="city live in",max_length=30,null= True)
    gender = models.CharField(verbose_name="gender",max_length=1,null= True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    def set_super(self,is_super):
        self.is_admin = is_super
        return
    
    def set_age(self):
        today = date.today()
        self.age = today.year - self.birth.year - ((today.month, today.day) < (self.birth.month, self.birth.day))
        return

    @property
    def is_staff(self):
        return self.is_admin
    
    def Get_city(self):
        return self.cityLiveIn
 




