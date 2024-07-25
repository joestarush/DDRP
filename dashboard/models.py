from django.db import models
from .manager import UserManager
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUser(AbstractUser):
    USER_TYPE_CHOICE = {
        'ad':'ADMIN',
        'vc':'VICTIM',
        'us':'USER'
    }
    username = None

    phone_number = models.CharField(max_length=10, unique = True)
    email = models.EmailField(verbose_name="Email", null=True, unique=True, max_length=100)


    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    user_type = models.CharField(max_length=2, choices=USER_TYPE_CHOICE, default='us')
    location = models.CharField(max_length = 256, null = True, blank = True)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return self.phone_number
    
class Index_page_info(models.Model):
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=256)
    image = models.ImageField(upload_to='static/index/info')

    def __str__(self):
        return self.title
    
class Requirements(models.Model):
    STATUS_INFO_CHOICE = {
        'ge' : 'GENERATED',
        'pn' : 'PENDING',
        'ac' : 'ACCEPTED',
        're' : 'RECEIVED',
        'se' : 'SENT'
    }

    CATEGORY_INFO_CHOICE = {
        'rf' : 'RAW VEGETABLES/ RAW FRUITS',
        'rs' : 'RAW SOLIDS',
        'wa' : 'WATER',
        'da' : 'DAIRY',
        'cl' : 'CLOTHES',
        'me' : 'MEDICINES',
        'sh' : 'SHELTER ITEMS'
    }

    id = models.IntegerField(primary_key=True)
    category = models.CharField(max_length=2, choices=CATEGORY_INFO_CHOICE)
    item = models.CharField(max_length=100)
    quantity = models.IntegerField()
    location = models.CharField(max_length=256)
    status = models.CharField(max_length=2, choices=STATUS_INFO_CHOICE)
    satisfied_by = models.CharField(max_length=10, blank=True)
    expiration_date = models.DateField(blank = True, null = True)
    satisfied_date = models.DateField(blank = True, null = True)
    needed_date = models.DateField()
    admin_id = models.CharField(max_length=10)
    current_location = models.CharField(max_length=256, blank = True, null = True)
    victim_id = models.CharField(max_length = 10, blank = True, null = True)

    def __str__(self):
        return str(self.id)

class Feedback(models.Model):
    name = models.CharField(max_length = 128)
    message = models.CharField(max_length= 256)
    image = models.ImageField(upload_to='static/index/feedback')
    
    def __str__(self):
        return self.name 
    
class Admin_additional_info(models.Model):
    phone_number = models.CharField(max_length=10, primary_key=True)
    email = models.EmailField(max_length= 256)
    aadhar_number = models.CharField(max_length=12)
    years_experience = models.IntegerField(default=0, blank=True)
    upload_photo = models.ImageField(upload_to='admin/dp')
    upload_aadhar = models.ImageField(upload_to='admin/aadhar')
    occupation = models.CharField(max_length=128, blank=True)
    def __str__(self):
        return self.phone_number
    
class Temp_admin_save(models.Model):
    phone_number = models.CharField(max_length=10, primary_key=True)
    upload_photo = models.ImageField(upload_to='admin/dp')
    upload_aadhar = models.ImageField(upload_to='admin/aadhar')

    def __str__(self):
        return self.phone_number
    
class temp_log_qr(models.Model):
    phone_number = models.CharField(max_length=10, unique = True)
    photo = models.ImageField(upload_to='qrcode/')
    