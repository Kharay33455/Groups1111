from django.shortcuts import render
from django.urls import reverse
from .models import *
from .models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.db import IntegrityError
from django.utils import timezone
from .forms import VerificationForm
from .forms import TestForm
# Create your views here.

def base(request):
    if request.user.is_authenticated:
        agent = Agent.objects.get(user = request.user)

        context = {"agent": agent, "time": timezone.now()}
        return render(request, 'base/index.html', context)
    else:

        context = {"time": timezone.now()}
        return render(request, 'base/index.html', context)

def profile(request, agent_id):
    agent = Agent.objects.get(pk = agent_id)
    agent_id = agent.id
    form = TestForm()
    context = {'agent':agent, 'form': form}
    return render(request, 'base/profile.html', context)

def register(request):
    if request.method == 'POST':
        
        first_name1 = request.POST['first_name']
        last_name1 = request.POST['last_name']
        username1 = request.POST['username']
        email1 = request.POST['email']
        number1 = request.POST['number']
        date1 = request.POST['dob']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        try:
            new_user = User.objects.create_user( username= username1, first_name = first_name1, last_name = last_name1, email = email1, password = password1)
            new_user.save()
            new_agent = Agent.objects.create(user = new_user, first_name = first_name1, last_name = last_name1, date_of_birth = date1, phone_number = number1)
            authenticated_user = authenticate(username = username1, password = password1)
            login(request, authenticated_user)
            return HttpResponseRedirect(reverse('base:base') )
        except (IntegrityError):
            context = {'err':'This user already exists'}
            return render (request, 'base/registration.html', context)
    else:



        return render(request, 'base/registration.html')
    
def logout_request(request):
    logout(request)

    return HttpResponseRedirect(reverse('base:base'))

def login_request(request):
    if request.method == 'POST':
        try:
            user = authenticate(request, username = request.POST['username'], password = request.POST['password1'])
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('base:base'))
            else:
                context = {'err':'Invalid username or password'}
                return render(request, 'base/login.html', context)
        except (KeyError, Agent.DoesNotExist):
            context = {'err':'User Does Not Exist'}
            return render(request, 'base/login.html', context)
    else:

        return render(request, 'base/login.html')
    
def verification_request(request, agent_id):
    agent = Agent.objects.get(pk = agent_id)
    if request.method == 'POST':
        form =  VerificationForm(request.POST, request.FILES)
        if form.is_valid():
            try:

                verification = form.save(commit = False)
                verification.user = request.user
                verification.agent = agent
                verification.save()
                verification_id = verification.id
                return HttpResponseRedirect(reverse('base:pending', args=(agent_id, verification_id)))
            except(IntegrityError):
                context = {'err': 'Your documents are already with us', 'agent':agent}
                return render(request, 'base/verification.html', context)
        else:
            return(render, 'base/verification.html', {'err':'Invalid documents'})
    else:
        try:
            agent = Agent.objects.get(pk = agent_id)

            verification = Verification.objects.get(user = request.user)
            context = {'agent': agent, 'verification': verification, 'err': 'You have completed the first step, leave the rest to us. Your verification is being processed.'}
            return render(request, 'base/pending.html', context)
        except (KeyError, Verification.DoesNotExist):




            agent = Agent.objects.get(pk =  agent_id)
            form = VerificationForm()
            context = {'agent':agent, 'form': form}
            return render(request, 'base/verification.html', context)
        
def verification_pending(request, agent_id, verification_id):
    agent = Agent.objects.get(pk = agent_id)
    verification = Verification.objects.get(pk = verification_id)
    context = {'agent':agent, 'verification': verification}
    return render(request, 'base/pending.html', context)


def policies(request):
    if request.user.is_authenticated:
        agent = Agent.objects.get(user = request.user)
        context = {'agent':agent}
        return render(request, 'base/policies.html', context)
    else:
        context = {}
        return render(request, 'base/policies.html', context)

def leaveamessage(request):
    if request.method == 'POST':
        if request.user.is_authenticated:

            agent = Agent.objects.get(user = request.user)
            title = request.POST['title']
            message = request.POST['message']
            new_messsage = Message.objects.create(agent = agent, title = title, message = message)
            new_messsage.save()
            context = {'agent': agent, 'msg':'Your message has been sent. We will reach out to you as soon as possible.'}
            return render(request, 'base/leavemessage.html', context)
        else:
            return HttpResponseRedirect(reverse('base:login'))
    else:



        if request.user.is_authenticated:
            agent = Agent.objects.get(user = request.user)
            context = {'agent': agent}
            return render(request, 'base/leavemessage.html', context)
        
        else:
            context = {}
            return render(request, 'base/leavemessage.html', context)