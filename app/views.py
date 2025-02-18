from django.shortcuts import render

from django.http import HttpResponse,HttpResponseRedirect
# Create your views here.
from app.forms import *
from app.models import *

from django.core.mail import send_mail

from django.contrib.auth import authenticate,login,logout
from django.urls import reverse

from django.contrib.auth.decorators import login_required




def registration(request):
    EUMFDO=UserMF()
    EPMFDO=ProfileMF()
    if request.method=='POST' and request.FILES:
        NMUMFDO=UserMF(request.POST)
        NMPMFDO=ProfileMF(request.POST,request.FILES)
        if NMUMFDO.is_valid() and NMPMFDO.is_valid():
            MUMFDO=NMUMFDO.save(commit=False)
            password=NMUMFDO.cleaned_data['password']
            MUMFDO.set_password(password)
            MUMFDO.save()

            MPMFDO=NMPMFDO.save(commit=False)
            MPMFDO.user_name=MUMFDO
            MPMFDO.save()

            send_mail('Registeration','Registration Successfull....','adarsh.vinod.3762@gmail.com',
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
        username=request.POST['username']        # Collecting the data
        password=request.POST['password']
        AUO=authenticate(username=username,password=password)      #Authenticating the data and storing in AUO
        if AUO:                                                    #Checking data is there in database or not
            if AUO.is_active:                                      #Checking whether its active or not
                login(request,AUO)                                 #Creating Login req
                request.session['username']=username               #Creating Session
                return HttpResponseRedirect(reverse('home'))       #Navigating to home page
            else:
                return HttpResponse('Not Active')
        else:
            return HttpResponse('Invalid Credentials')

    return render(request,'user_login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))