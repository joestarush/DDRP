import base64
import io
import json
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from .models import Index_page_info, Requirements, Feedback, Admin_additional_info, Temp_admin_save, temp_log_qr
from django.contrib import messages
import re
import smtplib
import random
import string
from django.contrib.auth import authenticate, login, logout
from captcha.image import ImageCaptcha
from django.utils.timezone import localtime
from PIL import Image,ImageDraw,ImageFont
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os 
from pathlib import Path
import qrcode
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt
from .forms import PhotoForm
import cv2
from datetime import timedelta, datetime




BASE_DIR = Path(__file__).resolve().parent.parent

# Create your views here.

User = get_user_model()

def dashboard(request):
    if request.method == 'POST' and request.user.user_type == 'us':
        request.session['requirement_id'] = request.POST['donate_now']
        return redirect('donate_now')
    
    if request.method == 'POST' and request.user.user_type == 'ad':
        request.session['requirement_id'] = request.POST['approve_now']
        return redirect('approve_now')
    
    else:
        feedback = Feedback.objects.all()[::-1]
        requirement = Requirements.objects.all()
        index_info = Index_page_info.objects.all()
        total_requirement = Requirements.objects.exclude(status = 're').count() 
        total_donated = Requirements.objects.filter(status = 're').count()
       
        data = []
        for i in ['rf', 'rs', 'wa', 'da', 'cl', 'me', 'sh']:

            data_count = Requirements.objects.filter(category = i).count()
            data.append(data_count)

        data2 = []
    
        for i in range(1, 8):
            data_2 = Requirements.objects.filter(satisfied_date__week_day=i).count()
            data2.append(data_2)
    
        data3 = []

        for i in range(1, 13):
            data_3 = Requirements.objects.filter(satisfied_date__month = i).count()
            data3.append(data_3)

        context = {'feedback':feedback, 
                'index_info':index_info,
                'requirement_items': requirement,
                'total_requirement' : total_requirement, 
                'total_donated' : total_donated,
                'data' : data,
                'data2' : data2,
                'data3' : data3,
                }
        return render(request, 'index.html',context)

def admin_signup(request):

    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last-name']
        email = request.POST['email']
        phone_number = request.POST['phone']
        aadhar = request.POST['aadhar']
        aadhar_file = request.FILES['aadhar-file']
        experience = request.POST['experience']
        occupation = request.POST['occupation']
        photo = request.FILES['photo']
        
        # checks if email is valid
        if is_valid_email_regex(email) == True:
            
            # checks if email exists in database:
            if User.objects.filter(email = email).exists() == False:
                
                # checks if valid phone number
                if is_valid_phone_number(phone_number) == True:
                    
                    # checks if phone number exists in database
                    if User.objects.filter(phone_number = phone_number).exists() == False:
                        request.session['first_name'] = first_name
                        request.session['last-name'] = last_name
                        request.session['email'] = email
                        request.session['phone'] = phone_number
                        request.session['aadhar'] = aadhar
                        request.session['experience'] = experience
                        request.session['occupation'] = occupation
                        temp_images_variable = Temp_admin_save(phone_number, photo, aadhar_file)
                        temp_images_variable.save()
                        return redirect('admin_otp')
                    
                    else:
                        error_text = "Phone number already exists in database"  
                        messages.info(request, error_text)
                        return redirect('admin_signup') 
                else:
                    error_text = "Phone number provided is not valid"
                    messages.info(request, error_text)
                    return redirect('admin_signup')  
            else:
                error_text = "Email provided already exists in database"
                messages.info(request, error_text)
                return redirect('admin_signup') 
        else:
            error_text = "Email provided is not valid"
            messages.info(request, error_text)
            return redirect('admin_signup')             
    
    else:
        return render(request, 'be_an_admin.html')

def victim_signup(request):
    if request.method == 'POST':
        global captcha
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        password = request.POST['password']
        gotten_captcha = request.POST['captcha']
        if captcha == gotten_captcha:
        
            # checks if email is valid
            if is_valid_email_regex(email) == True:
                
                # checks if email exists in database:
                if User.objects.filter(email = email).exists() == False:
                    
                    # checks if valid phone number
                    if is_valid_phone_number(phone_number) == True:
                        
                        # checks if phone number exists in database
                        if User.objects.filter(phone_number = phone_number).exists() == False:
                            request.session['first_name'] = first_name
                            request.session['last_name'] = last_name
                            request.session['email'] = email
                            request.session['phone_number'] = phone_number
                            request.session['password'] = password
                            return redirect('victim_otp')
                        
                        else:
                            error_text = "Phone number already exists in database"  
                            messages.info(request, error_text)
                            return redirect('victim_signup') 
                    else:
                        error_text = "Phone number provided is not valid"
                        messages.info(request, error_text)
                        return redirect('victim_signup')  
                else:
                    error_text = "Email provided already exists in database"
                    messages.info(request, error_text)
                    return redirect('victim_signup') 
            else:
                error_text = "Email provided is not valid"
                messages.info(request, error_text)
                return redirect('victim_signup')  
        else:
            error_text = "Captcha does not match"  
            messages.info(request, error_text)
            return redirect('victim_signup')        
    else:
        captcha = generate_img_captcha()
        print(captcha)
        return render(request, 'signup.html')

def victim_otp(request):
    first_name = request.session['first_name']
    last_name = request.session['last_name']
    email = request.session['email']
    phone_number = request.session['phone_number']
    password = request.session['password']

    if request.method == 'POST':
        global sent_otp
        d1 = request.POST['digit1']
        d2 = request.POST['digit2']
        d3 = request.POST['digit3']
        d4 = request.POST['digit4']
        d5 = request.POST['digit5']
        d6 = request.POST['digit6']
        
        if d1 == sent_otp[0] and d2 == sent_otp[1] and d3 == sent_otp[2] and d4 == sent_otp[3] and d5 == sent_otp[4] and d6 == sent_otp[5]:
            user1 = User(first_name = first_name, last_name = last_name, email = email, phone_number = phone_number, user_type = 'vc') 
            user1.set_password(password)
            user1.save()

            user = authenticate(request, phone_number = phone_number, password = password)
            login(request, user)
            return redirect('currloc')
        else:
            return redirect('victim_signup')
    else:    
        sent_otp = sent_otp_mail(request, 'victim')
        return render(request, 'otp.html', context = {'email':email, 'phone_number':phone_number})

def user_signup(request):
    if request.method == 'POST':
        global captcha
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        password = request.POST['password']
        gotten_captcha = request.POST['captcha']
        print(gotten_captcha)
        if captcha == gotten_captcha:
        
            # checks if email is valid
            if is_valid_email_regex(email) == True:
                
                # checks if email exists in database:
                if User.objects.filter(email = email).exists() == False:
                    
                    # checks if valid phone number
                    if is_valid_phone_number(phone_number) == True:
                        
                        # checks if phone number exists in database
                        if User.objects.filter(phone_number = phone_number).exists() == False:
                            request.session['first_name'] = first_name
                            request.session['last_name'] = last_name
                            request.session['email'] = email
                            request.session['phone_number'] = phone_number
                            request.session['password'] = password
                            return redirect('user_otp')
                        
                        else:
                            error_text = "Phone number already exists in database"  
                            messages.info(request, error_text)
                            return redirect('user_signup') 
                    else:
                        error_text = "Phone number provided is not valid"
                        messages.info(request, error_text)
                        return redirect('user_signup')  
                else:
                    error_text = "Email provided already exists in database"
                    messages.info(request, error_text)
                    return redirect('user_signup') 
            else:
                error_text = "Email provided is not valid"
                messages.info(request, error_text)
                return redirect('user_signup')  
        else:
            error_text = "Captcha does not match"  
            messages.info(request, error_text)
            return redirect('user_signup')        
    else:
        captcha = generate_img_captcha()
        print(captcha)
        return render(request, 'signup.html')

def user_otp(request):
    first_name = request.session['first_name']
    last_name = request.session['last_name']
    email = request.session['email']
    phone_number = request.session['phone_number']
    password = request.session['password']

    if request.method == 'POST':
        global sent_otp
        d1 = request.POST['digit1']
        d2 = request.POST['digit2']
        d3 = request.POST['digit3']
        d4 = request.POST['digit4']
        d5 = request.POST['digit5']
        d6 = request.POST['digit6']
        
        if d1 == sent_otp[0] and d2 == sent_otp[1] and d3 == sent_otp[2] and d4 == sent_otp[3] and d5 == sent_otp[4] and d6 == sent_otp[5]:
            user1 = User(first_name = first_name, last_name = last_name, email = email, phone_number = phone_number, user_type = 'us') 
            user1.set_password(password)
            user1.save()

            user = authenticate(request, phone_number = phone_number, password = password)
            login(request, user)
            return redirect('currloc')
        else:
            return redirect('user_signup')
    else:    
        sent_otp = sent_otp_mail(request, 'donator')
        return render(request, 'otp.html', context = {'email':email, 'phone_number':phone_number})

def is_valid_phone_number(phone_number):
    pattern = r'[6-9]\d{9}$'
    return bool(re.match(pattern, phone_number))

def is_valid_email_regex(email):
    # Regex pattern for basic email format validation
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(email_regex, email))

def admin_otp(request):
    first_name = request.session['first_name']
    last_name = request.session['last-name']
    email = request.session['email']
    phone_number = request.session['phone']
    aadhar = request.session['aadhar']
    experience = request.session['experience']
    occupation = request.session['occupation']

    if request.method == 'POST':
        global sent_otp
        d1 = request.POST['digit1']
        d2 = request.POST['digit2']
        d3 = request.POST['digit3']
        d4 = request.POST['digit4']
        d5 = request.POST['digit5']
        d6 = request.POST['digit6']
        
        if d1 == sent_otp[0] and d2 == sent_otp[1] and d3 == sent_otp[2] and d4 == sent_otp[3] and d5 == sent_otp[4] and d6 == sent_otp[5]:
            admin1 = User(first_name = first_name, last_name = last_name, email = email, phone_number = phone_number, user_type = 'ad') 
            temp_var = Temp_admin_save.objects.filter(phone_number = phone_number).values('upload_photo','upload_aadhar')
            admin2 = Admin_additional_info(phone_number = phone_number, email = email,aadhar_number = aadhar, years_experience = experience, upload_photo = temp_var[0]['upload_photo'], upload_aadhar = temp_var[0]['upload_aadhar'], occupation = occupation)
            password = getRandomPassword()
            admin1.set_password(password)
            send_admin_password(request, password)
            admin1.save()
            admin2.save()
            Temp_admin_save.objects.filter(phone_number = phone_number).delete()

            return redirect('currloc')
        else:
            return redirect('admin_signup')
    else:    
        sent_otp = sent_otp_mail(request, 'admin')
        return render(request, 'otp.html', context = {'email':email, 'phone_number':phone_number})

def sent_otp_mail(request, user_type):
    name = request.session['first_name']
    otp = generate_otp()

    smtp_object = smtplib.SMTP("smtp.gmail.com", 587)
    smtp_object.ehlo()
    smtp_object.starttls()
    our_email = 'mail.ddrp@gmail.com'
    password = 'gsmr clrh zqtt gqju'
    smtp_object.login(our_email, password)

    from_addr = our_email
    to_addr = request.session['email']

    subject = f'One-Time Password for {user_type} at ddrp.in'
    body = f'''Hi {name},
You recently requested a one-time password (OTP) create an account as {user_type}.

Your OTP is: {otp}

Please note: This OTP will expire in 3 min for security reasons. Please do not share this code with anyone.

If you did not request an OTP, please ignore this email.

Thanks,

The DDRP Team
'''
    message = 'Subject: '+subject+'\n' + body
    smtp_object.sendmail(from_addr, to_addr, message)
    smtp_object.quit()
    return otp

def generate_img_captcha():
    image = ImageCaptcha(font_sizes = (50,))
    captcha_text = generate_captcha()
    image.write(captcha_text, 'static/captcha/captcha-image.jpg')
    return captcha_text

def generate_captcha(length=4):
    characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    captcha = ''.join(random.choice(characters) for _ in range(length))
    return str(captcha)

def generate_otp(length = 6):
    characters = "0123456789"
    captcha = ''.join(random.choice(characters) for _ in range(length))
    return str(captcha)

def send_admin_password(request, admin_password):
    name = request.session['first_name']
    smtp_object = smtplib.SMTP("smtp.gmail.com", 587)
    smtp_object.ehlo()
    smtp_object.starttls()
    our_email = 'mail.ddrp@gmail.com'
    password = 'gsmr clrh zqtt gqju'
    smtp_object.login(our_email, password)

    from_addr = our_email
    to_addr = request.session['email']

    subject = f'Password for admin login at ddrp.in'
    body = f'''Hi {name},

Welcome to ddrp.in as admin!

Your password to access ddrp.in is {admin_password}

**Important:**

* This temporary password will expire after a certain period (check DDRP.in for details).
* Once retrieved, change your password to a strong and memorable one.

Thanks,

The DDRP Team
'''
    message = 'Subject: '+subject+'\n' + body
    smtp_object.sendmail(from_addr, to_addr, message)
    smtp_object.quit()

def getRandomPassword(length = 10):
    # Define character sets for different categories
    digits = string.digits
    uppercase = string.ascii_uppercase
    lowercase = string.ascii_lowercase

    # Combine all character sets for random selection
    all_characters = digits + uppercase + lowercase

    # Ensure at least one character from each category
    password = random.choice(digits) + random.choice(uppercase) + random.choice(lowercase)

    # Fill remaining characters with random selection from all characters
    password += ''.join(random.choices(all_characters, k=length - 3))

    # Shuffle the characters for better randomness (optional)
    random.shuffle(list(password))
    password = ''.join(password)

    return password

def signin(request):
    if request.method == 'POST':
        phone_number = request.POST['uname']
        password = request.POST['psw']
        user = authenticate(request, phone_number = phone_number, password = password)
        if user is not None:
            login(request, user)
            return redirect('currloc')
        else:
            return redirect('signin')
    
    else:
        return render(request, 'signin.html')

def forgot_password(request):
    return render(request, 'forgotpass.html')

def signout(request):
    logout(request)
    return redirect('dashboard')


def generate_requirements_admin(request):
    requirement = Requirements.objects.all()
    id = requirement.latest('id').id
    id += 1
    print(id)

    if request.method == 'POST':
        print(request.POST['category'])
        category = request.POST['category']
        item = request.POST['item']
        quantity = request.POST['quantity']
        location = request.POST['location']
        needed_date = request.POST['needed_date']
        requirement1 = Requirements(id = id, category = category, item = item, quantity = quantity, location = location, status = 'pn', needed_date = needed_date)
        requirement1.save()
        return redirect('generate_requirements_admin')

    else:
        context = {
            'id' : id 
        }
        return render(request, 'reqadminform.html', context)

def view_requirements(request):
    requirement = Requirements.objects.all()
    
    context = {
        'requirement_items': requirement
    }
    return render(request, 'view_requirements_table_full_page.html', context = context)

def track_requirements(request):
    if 'back' in request.POST:
        return redirect('dashboard')
    
    else:
        user =  request.user.phone_number
        requirement1 = Requirements.objects.filter(satisfied_by = user)
        context = {
            'requirements':requirement1
        }
        return render(request, 'track_requirements.html', context)

def log_requirements(request):
    
    if 'log_camera' in request.POST:
        return redirect('log_camera')

    if request.method == 'POST':
        id = request.POST['donator-id']
        print(id)
        today = localtime().date()
        
        requirement1 = Requirements.objects.filter(id = id).update(satisfied_date = today, status = 're')
        phone_number = Requirements.objects.get(id = id).satisfied_by
        
        first_name = User.objects.get(phone_number = phone_number).first_name
        last_name = User.objects.get(phone_number = phone_number).last_name
        email = User.objects.get(phone_number = phone_number).email
        certificate_make(f'{first_name} {last_name}')
        send_certificate(first_name, email)
        return redirect('dashboard')
    else:
        context = {

        }
        return render(request, 'log_requirements.html', context)
    

def donate_now(request):
    if 'back' in request.POST:
        return redirect('dashboard')
    
    if request.method == 'POST' and 'confirm' in request.POST:
        global id
        requirements1 = Requirements.objects.filter(id = id).update(status = 'ac', satisfied_by = request.user.phone_number)
        send_logging_mail(request, request.user.first_name, id)
        return redirect('dashboard')
    else:
        id = request.session['requirement_id']
        requirements1 = Requirements.objects.filter(id = id)
        context = {
            'requirements': requirements1
        }

        return render(request, 'donate_now.html', context)

def send_logging_mail(request, name, id):
    
    generate_requirements_qrcode('U', id)

        
    requirement1 = Requirements.objects.get(id = id)
    item = requirement1.item

    subject = f' Thank You for Your Donation to ddrp.in!'
    body = f'''Dear {name},
Thank you so much for confirming your donation of {item} to DDRP.in! Your generosity will directly support our vital work.

To complete your donation:

Please bring the following QR code with you when you visit base station to donate:

OR

You can provide the admin station attendant with the following requirement id {id}. 
We appreciate your support!
Sincerely,

The DDRP Team
'''
    sender_email = "mail.ddrp@gmail.com"
    recipient_email = request.user.email
    sender_password = "gsmr clrh zqtt gqju"
    smtp_server = 'smtp.gmail.com'
    smtp_port = 465

    path_to_file = os.path.join(Path(__file__).parent.parent, 'static','qrcode','qrcode.png')

    message = MIMEMultipart()
    message['Subject'] = subject
    message['From'] = sender_email
    message['To'] = recipient_email
    body_part = MIMEText(body)
    message.attach(body_part)

    with open(path_to_file,'rb') as file:
        
        message.attach(MIMEApplication(file.read(), Name='qrcode.png'))

    with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, message.as_string())
        server.quit()
   

def certificate_make(name):

    img = Image.open('static/certificate/CertificateTemplate.png')
    img = img.resize((800, 600))
    I1 = ImageDraw.Draw(img)
    font = ImageFont.truetype('static/certificate/font.ttf', 50) 
    I1.text((266, 410), name, font = font,fill="#000")
    I1.text((705,26),"12309",fill="#000")
    img.save("static/certificate/certificate_new.png")


def send_certificate(name, email):
    subject = "DDRP Donation Confirmation and Certificate Download"
    body = f'''Dear {name},

Thank you for your generous donation to DDRP.in! Your contribution will make a significant difference.

We are delighted to inform you that your donation has been successfully processed. You can download your donation certificate from the attachement below as a token of our appreciation for your support."
Sincerely,

The DDRP Team
'''
    sender_email = "mail.ddrp@gmail.com"
    recipient_email = email
    sender_password = "gsmr clrh zqtt gqju"
    smtp_server = 'smtp.gmail.com'
    smtp_port = 465
    path_to_file = os.path.join(Path(__file__).parent.parent, 'static','certificate','certificate_new.png')
    
    message = MIMEMultipart()
    message['Subject'] = subject
    message['From'] = sender_email
    message['To'] = recipient_email
    body_part = MIMEText(body)
    message.attach(body_part)

    with open(path_to_file,'rb') as file:
        
        message.attach(MIMEApplication(file.read(), Name='certificate.png'))

    with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, message.as_string())
        server.quit()

def generate_requirements_qrcode(user_type,requirement_id):

    img = qrcode.make(user_type+str(requirement_id))
    img.save(os.path.join(BASE_DIR, 'static', 'qrcode', 'qrcode.png'))

@login_required
def currloc(request):
    # Check if location data is submitted in POST request
    if request.method == 'POST':
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        if latitude and longitude:
            user1 = User.objects.filter(phone_number = request.user.phone_number).update(location = f'{latitude} {longitude}')
            return redirect('dashboard')  # Redirect to dashboard after saving location
    else:
        return render(request, 'currloc.html')

def victim_generate(request):
    
    requirement = Requirements.objects.all()
    id = requirement.latest('id').id
    location = request.user.location
    id += 1

    if request.method == 'POST':
        category = request.POST['category']
        item = request.POST['item']
        quantity = request.POST['quantity']
        location = request.POST['location']
        needed_date = request.POST['needed_date']
        requirement1 = Requirements(id = id, category = category, item = item, quantity = quantity, location = location, status = 'ge', needed_date = needed_date, victim_id = request.user.phone_number)
        requirement1.save()
        generate_victim_requirement_mail(request, request.user.first_name ,id)
        return redirect('dashboard')

    else:
        context = {
            'id' : id ,
            'loc' : location
        }
        return render(request, 'victim_generate_requirements.html', context)
    


def convert_coordinates(loc):
    loc = loc.split(' ')
    return loc

def generate_victim_requirement_mail(request, name, id):
    
    generate_requirements_qrcode('V', id)

        
    requirement1 = Requirements.objects.get(id = id)
    item = requirement1.item

    subject = f'Your Request on DDRP.in Has Been Submitted!'
    body = f'''Dear {name},
Thank you for submitting a request on DDRP.in! We appreciate you reaching out to us.

Your request of {item} is currently under review by our admins and will be processed as soon as possible. You will receive a notification once your request has been approved.

To ensure smooth delivery, please provide the following QR code to the admin team when they contact you.

Sincerely,

The DDRP.in Team
'''    

    sender_email = "mail.ddrp@gmail.com"
    recipient_email = request.user.email
    sender_password = "gsmr clrh zqtt gqju"
    smtp_server = 'smtp.gmail.com'
    smtp_port = 465

    path_to_file = os.path.join(Path(__file__).parent.parent, 'static','qrcode','qrcode.png')

    message = MIMEMultipart()
    message['Subject'] = subject
    message['From'] = sender_email
    message['To'] = recipient_email
    body_part = MIMEText(body)
    message.attach(body_part)

    with open(path_to_file,'rb') as file:
        
        message.attach(MIMEApplication(file.read(), Name='qrcode.png'))

    with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, message.as_string())
        server.quit()
   
def approve_now(request):
    if 'back' in request.POST:
        return redirect('dashboard')
    
    if request.method == 'POST' and 'confirm' in request.POST:
        global id
        requirements1 = Requirements.objects.filter(id = id).update(status = 'pn', admin_id = request.user.phone_number)
        victim_phone_number = Requirements.objects.get(id = id).victim_id
        first_name = User.objects.get(phone_number = victim_phone_number).first_name
        email = User.objects.get(phone_number = victim_phone_number).email

        approve_now_mail(request, name = first_name, email = email)
        return redirect('dashboard')
    else:
        id = request.session['requirement_id']
        requirements1 = Requirements.objects.filter(id = id)
        context = {
            'requirements': requirements1
        }

        return render(request, 'approve_now.html', context)

def track_requirements_victim(request):
    if 'back' in request.POST:
        return redirect('dashboard')
    
    else:
        user =  request.user.phone_number
        requirement1 = Requirements.objects.filter(victim_id = user)
        context = {
            'requirements':requirement1
        }
        return render(request, 'track_requirements_victim.html', context)
    
def approve_now_mail(request, name, email):
    
    smtp_object = smtplib.SMTP("smtp.gmail.com", 587)
    smtp_object.ehlo()
    smtp_object.starttls()
    our_email = 'mail.ddrp@gmail.com'
    password = 'gsmr clrh zqtt gqju'
    smtp_object.login(our_email, password)

    from_addr = our_email
    to_addr = email

    subject = f'Great News! Your DDRP.in Request Has Been Approved!'
    body = f'''Dear {name},
We have fantastic news! Your request on DDRP.in has been reviewed and approved by our admin team.

We understand your situation and are committed to helping you. However, fulfilling your request now depends on the generosity of a donor. We're actively searching for a kind individual who can provide the items you need.

Sincerely,
The DDRP.in Team
'''
    message = 'Subject: '+subject+'\n' + body
    smtp_object.sendmail(from_addr, to_addr, message)
    smtp_object.quit()

def log_camera(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST)
        if form.is_valid():
            photo_data_url = form.cleaned_data['photoData']
            # Extract the base64 encoded image data
            header, encoded = photo_data_url.split(',')
            # Decode the base64 data
            data = base64.b64decode(encoded)
            # Create a file-like object from the binary data
            file_io = io.BytesIO(data)
            # Create a ContentFile instance to save the file
            photo_file = ContentFile(file_io.read(), 'photo.png')

            print(photo_file)

            temp_log_qr.objects.all().delete()
            photo = temp_log_qr.objects.create(phone_number = request.user.phone_number, photo=photo_file)
            photo.save()

            file_name = temp_log_qr.objects.get(phone_number = request.user.phone_number).photo.name
            
            qr = scan_qr_code(file_name)
            today = localtime().date()

            if qr[0] == 'U':
                id = int(qr[1:])
                requirement1 = Requirements.objects.filter(id = id).update(satisfied_date = today, status = 're', current_location = request.user.location)
                phone_number = Requirements.objects.get(id = id).satisfied_by
        
                first_name = User.objects.get(phone_number = phone_number).first_name
                last_name = User.objects.get(phone_number = phone_number).last_name
                email = User.objects.get(phone_number = phone_number).email
                certificate_make(f'{first_name} {last_name}')
                send_certificate(first_name, email)

            if qr[0] == 'V':
                id = int(qr[1:])
                requirement1 = Requirements.objects.filter(id = id).update(satisfied_date = today, status = 'se', current_location = request.user.location)

            return redirect('dashboard')
    else:
        form = PhotoForm()

    return render(request, 'log_camera.html', {'form': form})

def scan_qr_code(name):
    image_path = os.path.join(Path(__file__).parent.parent, 'media' , name)
    img = cv2.imread(image_path)
    detector = cv2.QRCodeDetector()
    data, bbox, _ = detector.detectAndDecode(img)
    return data

def fill_data(request):
    for id in range(1000, 1010):
        #Requirements.objects.create(id = id, status = 'se', )
        pass
    return HttpResponse("datafilled!!")

def send(request):
    if request.method == 'POST':
        id = request.POST['requirement-id']
        phone_number = Requirements.objects.get(id = id).victim_id
        first_name = User.objects.get(phone_number = phone_number).first_name
        last_name = User.objects.get(phone_number = phone_number).last_name
        to_email = User.objects.get(phone_number = phone_number).email


        name = f'{first_name} {last_name}'

        sendDroneEmail(phone_number, id)
        sendDroneOperatorEmailVictim(to_email , name)
        return redirect('dashboard')

    context = {
        'phone_number' : '8964961321',
        'name' : 'Tarush Saxena'
    }

    return render(request, 'send.html', context = context)

def sendDroneEmail(phone_number, id):

    smtp_object = smtplib.SMTP("smtp.gmail.com", 587)
    smtp_object.ehlo()
    smtp_object.starttls()
    our_email = 'mail.ddrp@gmail.com'
    password = 'gsmr clrh zqtt gqju'
    smtp_object.login(our_email, password)

    from_addr = our_email
    to_addr = 'tarush888@gmail.com'

    subject = f'Urgent Delivery Request'
    body = f'''Dear Tarush,

Please deliver the required items for Requirement ID: {id} to the following victim:

Phone Number: {phone_number}

Kindly adhere to the scheduled delivery time as mentioned in your confirmation email.

Thank you for your timely assistance.

Regards,
DDRP Team
'''
    message = 'Subject: '+subject+'\n' + body
    smtp_object.sendmail(from_addr, to_addr, message)
    smtp_object.quit()

def sendDroneOperatorEmailVictim(email , victim_name):

    smtp_object = smtplib.SMTP("smtp.gmail.com", 587)
    smtp_object.ehlo()
    smtp_object.starttls()
    our_email = 'mail.ddrp@gmail.com'
    password = 'gsmr clrh zqtt gqju'
    smtp_object.login(our_email, password)

    from_addr = our_email
    to_addr = email

    subject = f'Drone Delivery Incoming'
    body = f'''Dear {victim_name},
Your requested items are on their way via drone.

The drone is being operated by Tarush Saxena, who can be reached at 8964961321.

To confirm receipt of your items, please be ready to present the QR code to the drone operator.

Thank you for your patience.

Regards,
DDRP Team
'''
    message = 'Subject: '+subject+'\n' + body
    smtp_object.sendmail(from_addr, to_addr, message)
    smtp_object.quit()