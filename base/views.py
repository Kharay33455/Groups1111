from django.shortcuts import render
from django.urls import reverse
from .models import *
from .models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.db import IntegrityError
from django.utils import timezone
from .forms import VerificationForm
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
    context = {'agent':agent}
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
            
            return(render, 'base/verification.html', {'err':'Invalid documents', 'agent':agent})
    else:
        try:
            agent = Agent.objects.get(pk = agent_id)

            if agent.is_verified:
                try:
                    bank = BankAccount.objects.get(agent = agent)
                    context = {'agent':agent, 'bank':bank}
                    return render(request, 'base/pending_bank.html', context)
                except(KeyError, BankAccount.DoesNotExist):

                    verification=Verification.objects.get(user= request.user)
                    context = {'agent':agent, 'verification':verification}
                    return render(request, 'base/account.html', context)
            else:
                verification = Verification.objects.get(user = request.user)
                context = {'agent': agent, 'verification': verification, 'err': 'You have completed the first step, leave the rest to us. Your verification is being processed.'}
                return render(request, 'base/pending.html', context)
        except (KeyError, Verification.DoesNotExist):




            agent = Agent.objects.get(pk =  agent_id)
            form = VerificationForm()
            prompt = Prompt.objects.filter(agent = agent).first()
            context = {'agent':agent, 'form': form, 'prompt':prompt}
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
        
def add_bank(request):
    request.method == 'POST'
    if request.user.is_authenticated:

        agent = Agent.objects.get(user = request.user)
        bank = request.POST['bank_name']
        bank_c = str(bank)
        account_number = request.POST['account_number']
        account_type = request.POST['type']
        account_name = request.POST['account_name']

        bankname = BankName.objects.get(bank_code = bank_c)
        new_bank = BankAccount.objects.create(agent = agent, bank_name = bankname, account_number = str(account_number), account_name = account_name, account_type = account_type)
        new_bank.save()


        return HttpResponseRedirect(reverse('base:validating'))

    else:
        return HttpResponseRedirect(reverse('base:login'))
    
def pending_bank(request):
    if request.user.is_authenticated:
        agent = Agent.objects.get(user = request.user)
        bank = BankAccount.objects.filter(agent = agent).last()
        context = {'agent': agent, 'bank': bank}
        return render(request, 'base/pending_bank.html', context)

def load_banks(request):
    banks = {
        "001":"CENTRAL BANK OF NIGERIA","011":"FIRST BANK OF NIGERIA PLC","023":"NIGERIA INTERNATINAL BANK (CITIBANK)","030":"HERITAGE BANK","032":"UNION BANK OF NIGERIA PLC","033":"UNITED BANK FOR AFRICA PLC","035":"WEMA BANK PLC","044":"ACCESS BANK NIGERIA LTD","050":"ECOBANK NIGERIA PLC","057":"ZENITH INTERNATIONAL BANK LTD","058":"GUARANTY TRUST BANK PLC","060002":"FBNQuest Merchant Bank Limited","068":"STANDARD CHARTERED BANK NIGERIA LTD","070":"FIDELITY BANK PLC","076":"SKYE BANK PLC","082":"KEYSTONE BANK LTD","090118":"IBILE MFB","090121":"HASAL MICROFINANCE BANK","100":"SUNTRUST BANK","101":"PROVIDUS BANK","214":"FIRST CITY MONUMENT BANK","215":"UNITY BANK PLC","221":"STANBIC IBTC BANK PLC","232":"STERLING BANK PLC","301":"JAIZ BANK PLC","327":"PAGA","502":"RAND MERCHANT BANK","526":"PARALLEX MFB","552":"NPF Microfinance Bank","559":"CORONATION MERCHANT BANK","560":"Page MFBank","561":"New Prudential Bank","601":"FSDH MERCHANT BANK LIMI","608":"FINATRUST MICROFINANCE BANK","090267":"KUDA MICROFINANCE BANK","305":"OPAY" 

    }
    for code, name in banks.items():
        BankName.objects.create(bank_code = code, bank_name = name)

    return render(request, 'base/done.html', banks)