from django.shortcuts import render

from django.http import HttpResponse,HttpResponseRedirect
# Create your views here.
from app.forms import *
from app.models import *

from django.core.mail import send_mail

from django.contrib.auth import authenticate,login,logout
from django.urls import reverse

from django.contrib.auth.decorators import login_required

import random


def registration(request):
    EUMFDO=UserMF()
    EPMFDO=ProfileMF()
    if request.method=='POST' and request.FILES:                   #for data and files 
        NMUMFDO=UserMF(request.POST)                               #user details collected
        NMPMFDO=ProfileMF(request.POST,request.FILES)              #Profile details collected
        if NMUMFDO.is_valid() and NMPMFDO.is_valid():              #check its valid or not
            MUMFDO=NMUMFDO.save(commit=False)                      #data converted to modified and make commit=false
            password=NMUMFDO.cleaned_data['password']              #collect the password
            MUMFDO.set_password(password)                          #encryption of password
            MUMFDO.save()                                          #save permanently

            MPMFDO=NMPMFDO.save(commit=False)                      #data converted to modified and make commit=false
            MPMFDO.user_name=MUMFDO                                #transfer the data to Modified profile MF
            MPMFDO.save()                                          #save permanently

            send_mail('Registration','Registration Successfull....','adarsh.vinod.3762@gmail.com',
                        [MUMFDO.email],fail_silently=True)

            return HttpResponse('Registration is Successfull.......') 
        else:
            return HttpResponse('Invalid Data')
    d={'EUMFDO' : EUMFDO ,'EPMFDO':EPMFDO}
    return render(request,'registration.html',d)


def home(request):
    if request.session.get('username'):                         # if the session is created then get the data
        username=request.session.get('username')                # Assigning
        d={'username' : username}                               # creates dictionary
        return render(request,'home.html',d)
    return render(request,'home.html')



def user_login(request):
    if request.method=='POST':
        username=request.POST['username']                          # Collecting the data
        password=request.POST['password']                          # Collecting the data
        AUO=authenticate(username=username,password=password)      #Authenticating the data and storing in AUO
        if AUO:                                                    #Checking data is there in database or not
            if AUO.is_active:                                      #Checking whether its active or not
                login(request,AUO)                                 #Creating Login req
                request.session['username']=username               #Creating Session
                return HttpResponseRedirect(reverse('home'))       #Navigating to home page,HttpRR navigates to home page and reverse is responsible for carrying the data
            else:
                return HttpResponse('Not Active')
        else:
            return HttpResponse('Invalid Credentials')

    return render(request,'user_login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

@login_required
def profile_display(request):                         
    USN=request.session.get('username')               #Get the loggedin username
    UO=User.objects.get(username=USN)                 #In order to get the User object we should get the loggedin username
    PO=Profile.objects.get(user_name=UO)              #Some of the elements are also present in profile model,so get Profile object(PO) also,we connected using a common column with user object(UO)
    d={'UO':UO,'PO':PO}                                 
    return render(request,'profile_display.html',d)

@login_required
def change_password(request):
    if request.method=='POST':                         #Post method gets activated
        USN=request.session.get('username')            #Get the loggedin username
        UO=User.objects.get(username=USN)              #In order to get the User object we should get the loggedin usernam
        NP=request.POST['np']                          #collect the new password entered by user
        UO.set_password(NP)                            #encrypt the pssd and update it
        UO.save()                                      #Save it
        return HttpResponse('Password Changed Successfully..........')
    return render(request,'change_password.html')


def forgot_password(request):
    if request.method=='POST':
        EDO=request.POST['email']          
        request.session['reset_email']=EDO
        OTP=str(random.randint(10000, 99999))
        request.session['reset_otp']=OTP
        send_mail('Verification',f'Your OTP for Reset Password is {OTP}.Please do not share with anyone....','adarsh.vinod.3762@gmail.com',
                        [EDO],fail_silently=True)

        return HttpResponseRedirect(reverse('otp_verification'))
        
    return render(request,'forgot_password.html')

def otp_verification(request):
    if request.method=='POST':
        ENOTP=request.POST.get('otp')
        STOTP=request.session.get('reset_otp')

        if ENOTP==STOTP:
            return HttpResponseRedirect(reverse('reset_pssd'))
    return render(request,'otp_verification.html')

def reset_pssd(request):
    if request.method=='POST':
        ED=request.session.get('reset_email')
        UO=User.objects.filter(email=ED) 
        if UO:
            UO=UO[0]
            RSP=request.POST['rsp']
            UO.set_password(RSP)
            UO.save()
            return HttpResponseRedirect(reverse('user_login'))
        else:
            return HttpResponse('User Does Not Exist !!')
    return render(request,'reset_pssd.html')
