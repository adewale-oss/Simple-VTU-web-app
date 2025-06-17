import json
import re
import requests
from requests.structures import CaseInsensitiveDict
from django.db.models.query import QuerySet
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse, JsonResponse, request, response, HttpResponseRedirect
from django.contrib import messages
from  .models import *
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.hashers import check_password
from .forms import  LoginForm, RegistrationForm, PaymentForm, PasswordForm, PinCreationForm, PinUpdateForm, ElectricityForm
from django.contrib.auth.decorators import login_required
from django.core import serializers
import phonenumbers
from phonenumbers import carrier 
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from datetime import datetime
from datetime import date
import random
import uuid
from django.conf import settings



@login_required
def user(request):
    user = request.user
    notes = Transaction.objects.filter(user= user.username, notify=True).order_by('-date_ordered')[:4]
    
    ref = Referral.objects.filter(referrer=user.username).count()
    context = {
        'notes': notes,
        'ref': ref
    }
    return render(request, 'dashe/profile.html', context)

@login_required
def notifications(request):
    
    user= request.user
    trans = Transaction.objects.filter(user=user.username, notify=True).order_by('-date_ordered')
    notes = Transaction.objects.filter(user= user.username, notify=True).order_by('-date_ordered')[:4]
    
    context = {
        'trans' : trans,
        'notes': notes
    }
    
    return render(request, 'dashe/notifications.html', context)


def home(request):
    return render(request, 'index.html')
    
@login_required
def dashboard(request):
    user = request.user
    ref = Referral.objects.filter(referrer=user.username).count()
    if ReferralBonus.objects.filter(bonus='ref_bonus').exists():
        bonus = ReferralBonus.objects.get(bonus='ref_bonus')
    else:
        bonus = {'per_transaction': 1, 'per_upgrade': 500}
        
    if Message.objects.filter(name='message').exists():
        message = Message.objects.get(name='message')
    else:
        message = {'message': 'Welcome To Our Platform Dear User'}
    
    if PaystackCharge.objects.filter(name='charge').exists():
        rate = PaystackCharge.objects.get(name='charge')
    else:
        rate = {'rate': 3}
        
    if MonifyRate.objects.filter(name='rate').exists():
        charge= MonifyRate.objects.get(name='rate')
    else:
        charge = {'rate': 2 }
        
    if ManualBank.objects.filter(name='bank').exists():
        bank = ManualBank.objects.get(name='bank')
    else:
        bank = {'bank_name': 'Null', 'acc_no': '0000000000', 'acc_name': 'Null'}
    
    trans = Transaction.objects.filter(user= user.username).order_by('-date_ordered')[:3]
    
    notes = Transaction.objects.filter(user= user.username, notify=True).order_by('-date_ordered')[:4]
    
    context = {
        'ref': ref,
        'bonus': bonus,
        'message' : message,
        'rate' : rate,
        'bank' : bank,
        'trans' : trans,
        'charge': charge,
        'notes': notes
    }
    
    
    return render(request, 'dashe/dashboard.html', context)

def signup(request):
    if request.method == 'POST':
        
        form = RegistrationForm(request.POST)
        if form.is_valid():
        
            name = form.cleaned_data.get('name')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            phone_no = form.cleaned_data.get('phoneno')
            password1 = form.cleaned_data.get('password1')
            password2= form.cleaned_data.get('password2')
            referrer = form.cleaned_data.get('ref')
            
            
            if password1 == password2:
                if CustomUser.objects.filter(username=username).exists():
                    response = JsonResponse({'code': '400', 'error' :'Username Taken'})
                    return response
                elif len(name) < 3:
                    response = JsonResponse({'code': '400', 'error' :'Enter A Valid Name'})
                    return response
                elif len(username) < 3:
                    response = JsonResponse({'code': '400', 'error' :'Enter a valid Username'})
                    return response
                elif len(phone_no) != 11:
                    response = JsonResponse({'code': '400', 'error' :'Enter a valid phone no'})
                    return response
                elif len(password1) < 6:
                    response = JsonResponse({'code': '400', 'error' :'Password must be at least 6 characters'})
                    return response
                elif username == password1:
                    response = JsonResponse({'code': '400', 'error' :'Password and Username too similar'})
                    return response
                elif CustomUser.objects.filter(email=email).exists():
                    response = JsonResponse({'code': '400', 'error' :'Email already exist'})
                    return response
                else:
                    user=CustomUser.objects.create_user(name=name, username=username, email=email, phone_no=phone_no, password=password1)
                    user.save()
                    if referrer:
                        referral = Referral(referrer=referrer, referred=username)
                        referral.save()
                    return JsonResponse({'code':'200', 'success': '/login/'})
            else:
                response = JsonResponse({'code': '400', 'error' :'Passwords not matching'})
                return response
        else:
            response = JsonResponse({'code': '400', 'error' :'Invalid Registration'})
            print(form.errors)
            return response
    else:      
        return render(request, 'dashe/signup.html')
    
    
    

    
def login(request):
    if request.method=='POST':
       form = LoginForm(request.POST)
       if form.is_valid():
           username = form.cleaned_data['username']
           password = form.cleaned_data['password']
           print(username, password)
           user = authenticate(username=username, password=password)
           if user is not None:
               auth.login(request, user)
               #print('username '+ 'password')
               #return create_virtual_account(request)
               response = JsonResponse({"code": 200, "success": "/user/dashboard/"}) 
               return (response)
           else:
              response = JsonResponse({"code": 400, "error": "Invalid Credentials"}) 
              return (response)
       else:
            response = JsonResponse({"code": 400, "error": "Invalid Auth"}) 
            return (response)
    else:
        return render(request, 'dashe/login.html')




#@receiver(post_save, sender=CustomUser)
def create_virtual_account(request):
    user = request.user
    def create_id():
        num = random.randint(1,10)
        num_2 = random.randint(1,10)
        num_3 = random.randint(1,10)
        return str(num_2)+str(num_3)+str(uuid.uuid4())
    
    ident = create_id()
    
    while CustomUser.objects.filter(account_ref = ident).exists():
        ident = create_id()
                
                
    if len(user.account_number) < 10:
        url = "https://api.monnify.com/api/v1/auth/login"

        payload={}
        headers = {
        'Authorization': f'Basic {settings.MY_MONNIFY_KEY}'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        #print(response.text)
        resp = json.loads(response.text)
        token = resp['responseBody']['accessToken']
        user = request.user
        if token:
            print(token)
            uni = str(user.id)
            
            
            url = "https://api.monnify.com/api/v2/bank-transfer/reserved-accounts"

            payload = json.dumps({
            "accountReference": ident,
            "accountName": user.username,
            "currencyCode": "NGN",
            "contractCode": settings.CONTRACT_CODE,
            "customerEmail": user.email,
            "customerName": user.username,
            "getAllAvailableBanks": 'false',
            "preferredBanks": ["035"]
            })
            headers = {
            'Authorization': 'Bearer '+token,
            'Content-Type': 'application/json'
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            print(response.text)
            respo = json.loads(response.text)
            if 'responseBody' in respo:
                user.account_name = respo['responseBody']['accounts'][0]['accountName']
                user.account_number = respo['responseBody']['accounts'][0]['accountNumber']
                user.bank_name = respo['responseBody']['accounts'][0]['bankName']
                user.account_ref = respo['responseBody']['accountReference']
                user.save()
                response = JsonResponse({"code": 200, "success": "/user/dashboard/"}) 
                return (response)
            else:
                response = JsonResponse({"code": 200, "success": "/user/dashboard/"}) 
                return (response)
    else:
        response = JsonResponse({"code": 200, "success": "/user/dashboard/"}) 
        return (response)





        
        
        
@login_required
def logout(request):
    auth.logout(request);
    return redirect('home')


@login_required
def data(request):
    if request.method == 'POST' or 'GET':
        user = request.user
        if user.pin:
            notes = Transaction.objects.filter(user= user.username, notify=True).order_by('-date_ordered')[:4]
            networks= DataNetwork.objects.filter(is_active=True)
            context = {
                'networks': networks,
                'notes': notes 
            }
            return render(request, 'dashe/data.html', context)
        else:
            return redirect('pin')

@login_required
def datatype(request):
    if request.method =='POST':
        net = request.POST.get('network', None)
        #net= json.loads(request.body.decode('UTF-8'))
        network = DataNetwork.objects.get(network_id=net)
        
        types = list(DataPlanType.objects.filter(network=network, is_available=True).values('name', 'id'))       
        print(types)
        
        return JsonResponse(types, safe=False)


@login_required
def dataplan(request):
    if request.method =='POST':
        net = request.POST.get('network', None)
        typ = request.POST.get('type')
        #net= json.loads(request.body.decode('UTF-8'))
        network = DataNetwork.objects.get(network_id=net)
        user = request.user
        print(typ)
        
        
        if user.package == 'Diamond':
            dataplans = DataPlan.objects.filter(network=network, plan_type=typ, is_active=True).values('plan_id', 'name', 'diamond_price')
        elif user.package == 'Gold':
            dataplans = DataPlan.objects.filter(network=network, plan_type=typ, is_active=True).values('plan_id', 'name', 'gold_price')
        else:
            dataplans = DataPlan.objects.filter(network=network, plan_type=typ, is_active=True).values('plan_id', 'name', 'silver_price')           
        
        package = user.package;
        data_plan = []
        for data in dataplans:
             data_plan.append({
                 'id': data['plan_id'],
                 'plan': data['name'],
                 'amount': data[package+'_price'],
                 })
        
        response = {
                
                'dataplans': list(data_plan)
                
            }
        
        return JsonResponse(response)
    


from django.db import transaction as db_transaction

@login_required
def buy_data(request):
    if request.method == 'POST':
        network = request.POST['network']
        plan_id = request.POST['plan']
        b_number = request.POST['b_number']
        pin = request.POST['pin']
        
        time_str = datetime.today().strftime("%Y%m%d%H%M")
        
        def create_id():
            num = random.randint(1, 10)
            num_2 = random.randint(1, 10)
            num_3 = random.randint(1, 10)
            return str(num_3) + str(num_2) + str(uuid.uuid4())[:6]

        ident = time_str + create_id()

        # Ensure unique reference ID
        while Transaction.objects.filter(reference=ident).exists():
            ident = create_id()

        user = request.user

        # Lock user record inside a transaction
        with db_transaction.atomic():
            user = CustomUser.objects.select_for_update().get(id=user.id)

            if user.pin != pin:
                return JsonResponse({"code": 500, "error": 'Invalid PIN'})

            plan = DataPlan.objects.get(id=plan_id)
            plan_name = plan.name
            price = plan.user_price if user.package == 'user' else plan.agent_price

            if user.wallet_balance is None or user.wallet_balance == 0 or user.wallet_balance < int(price):
                return JsonResponse({"code": 500, "error": "Insufficient Balance"})

            if len(b_number) != 11:
                return JsonResponse({"code": 500, "error": "Invalid Mobile Number"})

            # Deduct balance and create transaction
            service = f'Data | {plan.network}'
            transaction = Transaction.objects.create(
                user=user.username,
                service=service,
                reference=ident,
                beneficiary=b_number,
                plan=plan_name,
                amount=price,
                amount_paid=price,
                bal_before=user.wallet_balance,
                bal_after=(user.wallet_balance - price),
                status="pending"
            )

            user.wallet_balance -= int(price)
            user.save()

        # Make API request outside the database lock
        url = "https://server.aibentopup.com/api/data/topup"
        payload = json.dumps({"id": plan.plan_id, "pin": settings.MY_PIN, "number": b_number})
        headers = {
            'Authorization': f'Bearer {settings.MY_API_KEY}',
            'Content-Type': 'application/json'
        }

        try:
            response = requests.post(url, headers=headers, data=payload)
            
            resp = json.loads(response.text)
    
            # Handle API Response
            resp_status = resp['status']

            if resp_status == 'success':
                status = 'success'
                # Handle referral bonus
                if Referral.objects.filter(referred=user.username).exists():
                    ref = Referral.objects.get(referred=user.username)
                    referrer = CustomUser.objects.get(username=ref.referrer)
                    bonus = ReferralBonus.objects.filter(bonus='ref_bonus').first()
                    bonus_amount = bonus.per_transaction if bonus else 1
                    referrer.referal_bonus += bonus_amount
                    referrer.save()
            elif resp_status == 'failed':
                status = 'failed'

                # Refund user inside a transaction
                with db_transaction.atomic():
                    user = CustomUser.objects.select_for_update().get(id=user.id)
                    user.wallet_balance += int(price)
                    user.save()
            elif resp_status == 'reversed':
                status = 'failed'

                # Refund user inside a transaction
                with db_transaction.atomic():
                    user = CustomUser.objects.select_for_update().get(id=user.id)
                    user.wallet_balance += int(price)
                    user.save()
            else:
                status = 'pending'

            # Update transaction status
            transaction.status = status
            transaction.message = f'Your purchase of {plan_name} for {b_number} is {"successful" if status == "success" else "failed"}'
            transaction.save()

        except Exception:
            # Handle request failure
            """
            with db_transaction.atomic():
                user = CustomUser.objects.select_for_update().get(id=user.id)
                user.wallet_balance += int(price)  # Refund
                user.save()
            """
            
            transaction.status = 'pending'
            transaction.message = f'Your purchase of {plan_name} for {b_number} status was not confirmed'
            transaction.save()

            return JsonResponse({"code": 500, "error": "Transaction failed, amount refunded"})

        

        return JsonResponse({"code": 200, "success": "Transaction Successful", 'pk': transaction.id})         
        
    

@login_required
def cable(request):
    if request.method == 'POST' or 'GET':
        user = request.user
        if user.pin:
            notes = Transaction.objects.filter(user= user.username, notify=True).order_by('-date_ordered')[:4]
            decoders = Decoder.objects.filter(is_active=True)
        
            context = {
                'notes': notes,
                'decoders': decoders
            }
            return render(request, 'dashe/cable.html', context)
        else:
            return redirect('pin')


@login_required
def cableplan(request):
    if request.method == 'POST':
        dec = request.POST['decoder']
        decoder = Decoder.objects.get(provider_id=dec)
        user = request.user
   
        if user.package == 'Diamond':
            cableplans = CablePlan.objects.filter(decoder=decoder, is_active=True).values('plan_id', 'name', 'diamond_price')
        elif user.package == 'Gold':
            cableplans = CablePlan.objects.filter(decoder=decoder, is_active=True).values('plan_id', 'name', 'gold_price')
        else:
            cableplans = CablePlan.objects.filter(decoder=decoder, is_active=True).values('plan_id', 'name', 'silver_price')           
        
        package = user.package;
        cable_plan = []
        for cable in cableplans:
             cable_plan.append({
                 'id': cable['plan_id'],
                 'plan': cable['name'],
                 'amount': cable[package+'_price'],
                 })
      
        context = {
            'cableplans':list(cable_plan)
     
        }
        return JsonResponse(context)
    

@login_required  
def verify_cable(request):
    if request.method == 'POST':
        decoder = request.POST['cable']
        card_no = request.POST['card_no']
        cable = Decoder.objects.get(provider_id = decoder)
        print(cable)
        print(card_no)
        
        url = "https://aslamfastsub.com.ng/api/validate.php?type=cable&cable="+cable.name+"&decoder="+card_no;

        payload={}
        files={}
        headers = {}

        resp = requests.request("GET", url, headers=headers, data=payload, files=files)
        response = json.loads(resp.text)
       
        return JsonResponse(response)
    
        
      
from django.db import transaction as db_transaction

def buy_cable(request):
    if request.method != 'POST':
        return JsonResponse({"code": 400, "error": "Invalid request method"})
    
    provider_id = request.POST.get('decoder')
    plan_id = request.POST.get('plan')
    card_no = request.POST.get('card_no')
    b_number = request.POST.get('b_number')
    b_name = request.POST.get('b_name')
    pin = request.POST.get('pin')
    
    # Generate Unique Transaction ID
    time_stamp = datetime.today().strftime("%Y%m%d%H%M")
    def create_id():
        return str(random.randint(1, 10)) + str(random.randint(1, 10)) + str(uuid.uuid4())[:6]
    
    ident = time_stamp + create_id()
    while Transaction.objects.filter(reference=ident).exists():
        ident = create_id()
    
    user = request.user
    if user.pin != pin:
        return JsonResponse({"code": 500, "error": "Invalid PIN"})
    
    # Get Plan & Price
    try:
        plan = CablePlan.objects.get(plan_id=plan_id)
    except CablePlan.DoesNotExist:
        return JsonResponse({"code": 400, "error": "Invalid Plan ID"})
    
    price = plan.user_price if user.package == 'user' else plan.agent_price
    
    # Ensure valid beneficiary number
    if len(b_number) != 11:
        return JsonResponse({"code": 500, "error": "Invalid Mobile Number"})
    
    try:
        decoder = Decoder.objects.get(provider_id=provider_id)
    except Decoder.DoesNotExist:
        return JsonResponse({"code": 400, "error": "Invalid Decoder ID"})
    
    # Lock user row during transaction processing
    with db_transaction.atomic():
        user = CustomUser.objects.select_for_update().get(id=user.id)  # Lock user row
        if user.wallet_balance is None or user.wallet_balance < int(price):
            return JsonResponse({"code": 500, "error": "Insufficient Balance"})
        
        # Deduct balance & Save Transaction
        user.wallet_balance -= int(price)
        user.save()
        
        service = 'Cable'
        transaction = Transaction(
            user=user.username,
            service=service,
            reference=ident,
            beneficiary=card_no,
            beneficiary_name=b_name,
            plan=plan.name,
            amount=price,
            amount_paid=price,
        )
        transaction.save()
    
    # Send API Request (Outside Locked Block to Avoid Long Lock Time)
    url = "https://server.aibentopup.com/api/cable/subscription"
    payload = json.dumps({
        "id": plan.plan_id,
        "pin": settings.MY_PIN,
        "number": b_number,
        "cardNumber": card_no
    })
    headers = {
        'Authorization': f'Bearer {settings.MY_API_KEY}',
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, data=payload)
    resp = json.loads(response.text)
    
    # Handle API Response
    resp_status = resp['status']
    if resp_status == 'failed':
        with db_transaction.atomic():
            user = CustomUser.objects.select_for_update().get(id=user.id)  # Lock user again
            user.wallet_balance += int(price)  # Refund user
            user.save()
        status = 'failed'
    elif resp_status == 'reversed':
        with db_transaction.atomic():
            user = CustomUser.objects.select_for_update().get(id=user.id)  # Lock user again
            user.wallet_balance += int(price)  # Refund user
            user.save()
        status = 'failed'
    elif resp_status == 'success':
        status = 'success'
    else:
        status = 'pending'
    
    # Update Transaction Status
    transaction.status = status
    transaction.message = f'Dear {b_name} ({card_no}), your purchase of {plan.name} is {status}'
    transaction.save()
    
    return JsonResponse({"code": 200, "success": "Transaction Successful", 'pk': transaction.id})  


@login_required
def electricity(request):
    user = request.user
    if request.method == 'POST' or 'GET':
        if request.user.pin:
            discos = Disco.objects.filter(is_active=True)
            notes = Transaction.objects.filter(user= user.username, notify=True).order_by('-date_ordered')[:4]
            context = {
                'discos': discos,
                'notes': notes
            }
            return render(request, 'dashe/electricity.html', context)
        else:
            return redirect('pin')

@login_required
def buy_electricity(request):
    if request.method == 'POST':
        disco = request.POST.get('disco')
        meter = request.POST.get('meter')
        amount = request.POST.get('amount')
        b_number = request.POST.get('b_number')
        pin = request.POST.get('pin')
        print(disco)
        
        
        time = datetime.today().strftime("%Y%m%d%H%M")
        def create_id():
            num = random.randint(1, 10)
            num_2 = random.randint(1, 10)
            num_3 = random.randint(1, 10)
            return str(num_3)+str(num_2)+str(uuid.uuid4())[:6]

        ident = time + create_id()
        
     
        while Transaction.objects.filter(reference = ident).exists():
            ident = create_id()
            
        disc = Disco.objects.get(id=disco) 
        
        user = request.user
        
        if user.package == 'Diamond':
            c_fee = disc.diamond_convinience_fee
        elif user.package == 'Gold':
            c_fee = disc.gold_convinience_fee
        else:
            c_fee = disc.silver_convinience_fee  
        print(c_fee)
        
        t_amount = int(amount) + c_fee
        if user.pin == pin:
            if user.wallet_balance != None:
                    if user.wallet_balance != '0':
                        if user.wallet_balance >= t_amount:
                            if int(amount) >= 1000:
                                if len(b_number) == 11:
                                    service = f'Electricity'
                                    transaction= Transaction(user=user.username, service=service, reference=ident, beneficiary=meter, plan=disc.name + ' ' +types, amount=amount, amount_paid=t_amount, status='initiated', bal_before=user.wallet_balance, bal_after=(user.wallet_balance - t_amount), convinience_fee=c_fee)
                                    transaction.save()
                                    
                                    user.wallet_balance -= t_amount
                                    user.save()
                                      
                                    
                                    """
                                    url = "https://us-central1-paybills-d74e3.cloudfunctions.net/app/api/apibuyelectricity"

                                    payload = json.dumps({
                                    "plan": disc.disco_id,
                                    "meter_number": card_no,
                                    "reference": ident,
                                    "amount": amount
                                    })
                                    headers = {
                                    'Authorization': f'Bearer {settings.MY_API_KEY}',
                                    'Content-Type': 'application/json'
                                    }
        
                                    response = requests.request("POST", url, headers=headers, data=payload)
        
                                    print(response.text)
                                    resp = json.loads(response.text)
                                
                                    resp_status = resp['status']
                                    token = resp['token']
                                    if resp_status == 'successful':
                                        status = 'success'
                                    elif resp_status == 'failed':
                                        status = 'failed'
                                        user.wallet_balance += int(price)
                                        user.save()
                                    else:
                                        status = 'pending'  

                                    """

                                    status = 'success'
                                    transaction.status= status
                                    transaction.message = f'Dear Customer, your payment of {amount} naira for ({meter}) {types} bill is successfully submited '
                                    transaction.save()
                                    
                                    return JsonResponse({"code": 200, 'success': 'successfully submitted', 'pk': transaction.id})
                                    
                                
                                
                                else:
                                    return JsonResponse({"code": 500, 'error': 'invalid Mobile Number'})
                            else:
                                return JsonResponse({"code": 500, 'error': 'Amount Can Only Be 1000 or Higher'})
                        else:
                            return JsonResponse({"code": 500, 'error': 'Insufficient Balance'})
                    else:
                        return JsonResponse({"code": 500, 'error': 'Insufficient Balance'})
            else:
                return JsonResponse({"code": 500, 'error': 'Insufficient Balance'})
        else:
            return JsonResponse({"code": 500, 'error': 'Invalid pin'})
        
@login_required
def verify_airtime_phone(request):
    if request.method == 'POST':
        phone_no = request.POST['b_number']
        service_provider = phonenumbers.parse("+234"+phone_no)
        net = str((carrier.name_for_number(service_provider, 'en')))
        network = str.upper(net)
        #print(str.upper(network))
        
        
        net = AirtimeNetwork.objects.get(name=network, is_available=True)
        types = list(Airtime.objects.filter(network=net, is_available=True).values('types'))
        #print(types)
        response = JsonResponse([{"network": network}, types], safe=False)
        return (response)
    
@login_required
def verify_phone(request):
    if request.method == 'POST':
        phone_no = request.POST['b_number']
        service_provider = phonenumbers.parse("+234"+phone_no)
        network = (carrier.name_for_number(service_provider, 'en'))
        
        
        response = JsonResponse({"network": network})
        return (response)
       

@login_required
def airtime(request):
    user = request.user
    if request.method == 'POST' or 'GET':
        if request.user.pin:
            networks = AirtimeNetwork.objects.filter(is_available=True)
            notes = Transaction.objects.filter(user= user.username, notify=True).order_by('-date_ordered')[:4]
            context = {
                'networks' : networks,
                'notes': notes
            }
            return render(request, 'dashe/airtime.html', context)
        else:
            return redirect('pin')

@login_required
def fetch_type(request):
    
    if request.method == 'POST':
        network = request.POST['network']
        
        net = AirtimeNetwork.objects.get(name=network, is_available=True)
        types = list(Airtime.objects.filter(network=net, is_available=True).values('types'))
        response = JsonResponse( types, safe=False)
        return (response)

@login_required
def fetch_amount(request):
    if request.method== 'POST':
        amount = request.POST['amount']
        network = request.POST['network']
        type = request.POST['type']
        
        user = request.user
        net = AirtimeNetwork.objects.get(name=network)
        rates = Airtime.objects.get(network=net, types=type)
        if user.package == 'Diamond':
            rate = rates.diamond_rate
        elif user.package == 'Gold':
            rate = rates.gold_rate
        else:
            rate = rates.silver_rate
        if amount.isdigit():
            print(rate)
            quotent = rate / 100
            t_amount = quotent * int(amount)
            
            return JsonResponse({'t_amount': t_amount})
            
        else:
            return JsonResponse({'code':500, 'error': 'Invalid Amount'})


from django.db import transaction as db_transaction

def buy_airtime(request):
    if request.method == 'POST':
        network = request.POST.get('network')
        amount = request.POST.get('amount')
        b_number = request.POST.get('b_number')
        a_type = request.POST.get('type')
        pin = request.POST.get('pin')
        user = request.user
        
        if not amount.isdigit() or int(amount) <= 0:
            return JsonResponse({'code': 500, 'error': 'Invalid Amount'})
        
        time = datetime.today().strftime("%Y%m%d%H%M")
        def create_id():
            return str(random.randint(100, 999)) + str(uuid.uuid4())[:6]
        
        ident = time + create_id()
        while Transaction.objects.filter(reference=ident).exists():
            ident = create_id()
        
        try:
            net = AirtimeNetwork.objects.get(name=network)
            rates = Airtime.objects.get(network=net.network_id, types=a_type)
        except AirtimeNetwork.DoesNotExist or Airtime.DoesNotExist:
            return JsonResponse({'code': 500, 'error': 'Invalid network or plan'})
        
        rate = rates.user_rate if user.package == 'user' else rates.agent_rate
        t_amount = (rate / 100) * int(amount)
        
        if pin != user.pin:
            return JsonResponse({'code': 500, 'error': 'Invalid pin'})
        
        if len(b_number) != 11:
            return JsonResponse({'code': 500, 'error': 'Invalid Mobile Number'})
        
        with db_transaction.atomic():
            user = CustomUser.objects.select_for_update().get(id=user.id)
            if user.wallet_balance is None or user.wallet_balance < t_amount:
                return JsonResponse({'code': 500, 'error': 'Insufficient Balance'})
            
            transaction_obj = Transaction(
                user=user.username, service='Airtime', reference=ident,
                plan=f'{network} {a_type}', beneficiary=b_number,
                amount=amount, amount_paid=t_amount,
                bal_before=user.wallet_balance,
                bal_after=(user.wallet_balance - t_amount)
            )
            transaction_obj.save()
            
            user.wallet_balance -= t_amount
            user.save()
        
        url = "https://server.aibentopup.com/api/airtime/topup"
        payload = json.dumps({
            "id": rates.plan_id,
            "pin": settings.MY_PIN,
            "number": b_number,
            "amount": amount
        })
        headers = {
            'Authorization': f'Bearer {settings.MY_API_KEY}',
            'Content-Type': 'application/json'
        }
        response = requests.post(url, headers=headers, data=payload)
        
        resp = json.loads(response.text)
    
        # Handle API Response
        resp_status = resp['status']
        if resp_status == 'failed':
            with db_transaction.atomic():
                user = CustomUser.objects.select_for_update().get(id=user.id)
                user.wallet_balance += t_amount
                user.save()
            status = 'failed'
        elif resp_status == 'reversed':
            with db_transaction.atomic():
                user = CustomUser.objects.select_for_update().get(id=user.id)
                user.wallet_balance += t_amount
                user.save()
            status = 'failed'
        elif resp_status == 'success':
            status = 'success'
        else:
            status = 'pending'    
        
        transaction_obj.status = status
        transaction_obj.message = f'Your purchase of {network} {a_type} airtime of {amount} naira for {b_number} is {status}'
        transaction_obj.save()
        
        return JsonResponse({'code': 200, 'success': 'Transaction Successful', 'pk': transaction_obj.id})   


@login_required
def transaction(request):
    user= request.user
    trans = Transaction.objects.filter(user=user.username).order_by('-date_ordered')
    notes = Transaction.objects.filter(user= user.username, notify=True).order_by('-date_ordered')[:4]
    
    context = {
        'trans' : trans,
        'notes': notes
    }
    
    return render(request, 'dashe/transactions.html', context)

@login_required
def transaction_detail(request, pk):
    user = request.user
    tran = get_object_or_404(Transaction, id=pk)
    notes = Transaction.objects.filter(user= user.username, notify=True).order_by('-date_ordered')[:4]
        
    context = {
        'tran' : tran,
        'notes': notes
    }
    return render(request, 'dashe/transaction-detail.html', context)


@login_required
def funding(request):
    return render(request, 'dashe/fund.html')

@login_required
def card(request):
    user = request.user
    notes = Transaction.objects.filter(user= user.username, notify=True).order_by('-date_ordered')[:4]
    if PaystackCharge.objects.filter(name='charge').exists():
        rate = PaystackCharge.objects.get(name='charge')
    else:
        rate = {'rate': 2}
        
    context= {
        'rate': rate,
        'notes': notes
    }
    return render(request, 'dashe/card.html', context)


@login_required
def payment(request):
    user = request.user
    if PaystackCharge.objects.filter(name='charge').exists():
        rate = PaystackCharge.objects.get(name='charge')
    else:
        rate = {'rate': 2}
    
    r = rate.rate / 100
    #print(r)
    if request.method == 'POST':
        
        form = PaymentForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data.get('amount')
            charge = int(amount) * r
            ini_amount = int(amount) + charge
            #print(ini_amount)
            #print(charge)
            
            total_amount = ini_amount * 100
            #print(total_amount)
            
            url = "https://api.paystack.co/transaction/initialize"

            payload={'email': user.email,
            'amount': total_amount}
            files=[

            ]
            headers = {
            'Authorization': 'Bearer sk_test_ea40d927962c05d1aea76c5410c470e535b70ba9',
            #'Cookie': 'sails.sid=s%3ANW-_PFGTQvwk3KBglmWeZFq3LXUV0wQX.w%2Fwz%2FPaVllqvXwELtRFprjehvzydT%2Fu8maM3kHiA%2Ftw'
            }

            response = requests.request("POST", url, headers=headers, data=payload, files=files)
            #print(response.text)
            resp = json.loads(response.text)
            #print(resp)
            link = resp['data']['authorization_url']
            #access_code = resp['data']['access_code']
            reference = resp['data']['reference']
            status = 'initiated'
            transaction= Transaction(user=user.username, service='Wallet Topup', amount=amount, status=status, route='Card Payment', reference=reference)
            paystack = Paystack(user=user.username, amount=amount, status=status, reference=reference)
            transaction.save()
            paystack.save()
            return JsonResponse(link, safe=False)
    
       
@login_required
def manual_funding(request):
    user = request.user
    notes = Transaction.objects.filter(user= user.username, notify=True).order_by('-date_ordered')[:4]
    if ManualBank.objects.filter(name='bank').exists():
        bank = ManualBank.objects.get(name='bank')
    else:
        bank = {'bank_name': 'Null', 'acc_no': '0000000000', 'acc_name': 'Null'}
    return render(request, 'dashe/manual.html', {'bank': bank, 'notes': notes})


@login_required
def bank_transfer(request):
    user = request.user
    notes = Transaction.objects.filter(user= user.username, notify=True).order_by('-date_ordered')[:4]
    context={
        'notes': notes
    }
    return render(request, 'dashe/bank.html')




@login_required
def upgrade(request):
    
    if UpgradePrice.objects.filter(name='price').exists():
        price = UpgradePrice.objects.get(name='price')
    else:
        price = {'agent': 2000}
    return render(request, 'dashboard/upgrade.html', {'price': price})




@login_required
def password(request):
    user = request.user
    notes = Transaction.objects.filter(user= user.username, notify=True).order_by('-date_ordered')[:4]
    if request.method=='POST':
        user = request.user
        form = PasswordForm(request.POST)
        if form.is_valid():
            old_pass= form.cleaned_data.get('old_pass')
            new_pass1 = form.cleaned_data.get('new_pass1')
            new_pass2 = form.cleaned_data.get('new_pass2')
            print(old_pass, new_pass1, new_pass2)
            
            check = check_password(old_pass, request.user.password)
            
            if check:
                if new_pass1 == '' or len(new_pass1) < 5:
                    return JsonResponse({'code':500, 'error': 'Input a minimum of 6 characters'})
                elif new_pass1 == new_pass2:
                    user.set_password(new_pass1)
                    user.save()
                    update_session_auth_hash(request, user)
                    #auth.logout(request);
                    return JsonResponse({'code':200, 'success': 'Password Changed Successfully', 'redirect' : '/user/dashboard/'})
                else:
                    return JsonResponse({'code':500, 'error': 'Passwords Not Matching'})
            else:
                return JsonResponse({'code':500, 'error': 'Old Password Not Correct'})
         
        else:
            return render(request, 'dashe/password.html', {'form':form, 'notes': notes})
    else:
        return render(request, 'dashe/password.html', {'notes': notes})
    

    


@login_required
def pin(request):
    user = request.user
    notes = Transaction.objects.filter(user= user.username, notify=True).order_by('-date_ordered')[:4]
    return render(request, 'dashe/pin.html', {'notes': notes})

@login_required
def create_pin(request):
    if request.method == 'POST':
        form = PinCreationForm(request.POST)
        if form.is_valid():
            pin1 = form.cleaned_data.get('pin1')
            pin2 = form.cleaned_data.get('pin2')
            if pin1 == pin2:
                if len(pin1) == 4:
                    user= request.user
                    user.pin = pin1
                    user.save()
                    return JsonResponse({'code':200, 'success': 'Pin created successfully'})
                else:
                    return JsonResponse({'code':500, 'error': 'Pin can only be 4 digits'})
            else:
                return JsonResponse({'code':500, 'error': 'Pin not matching'})
        else:
            return JsonResponse({'code':500, 'error': 'Something went wrong'})
    else:
        return JsonResponse({'code':500, 'error': 'Something went wrong'})


@login_required
def update_pin(request):
    if request.method == 'POST':
        form = PinUpdateForm(request.POST)
        if form.is_valid():
            u_pin1 = form.cleaned_data.get('u_pin1')
            u_pin2 = form.cleaned_data.get('u_pin2')
            password = form.cleaned_data.get('password')
            
            check = check_password(password, request.user.password)
            if check:
                if u_pin1 == u_pin2:
                    if len(u_pin1) == 4:
                        user= request.user
                        user.pin = u_pin1
                        user.save()
                        return JsonResponse({'code':200, 'success': 'Pin Updated successfully'})
                    else:
                        return JsonResponse({'code':500, 'error': 'Pin can only be 4 digits'})
                else:
                    return JsonResponse({'code':500, 'error': 'Pin not matching'})
            else:
                return JsonResponse({'code':500, 'error': 'Incorrect Password'})
        else:
            return JsonResponse({'code':500, 'error': 'Something went wrong'})
    else:
        return JsonResponse({'code':500, 'error': 'Something went wrong'})
    
    
@login_required
def success(request):
    return render(request, 'dashboard/success.html')



@require_POST
@csrf_exempt
def monify_update(request):
    
    if request.method == 'POST':
       resp = json.loads(request.body)
       
       ref = resp['eventData']['transactionReference']
       acc_no = resp['eventData']['destinationAccountInformation']['accountNumber']
       amount = resp['eventData']['amountPaid']
       email = resp['eventData']['customer']['email']
       
       if MonifyRate.objects.filter(name='rate').exists():
           charge= MonifyRate.objects.get(name='rate')
       else:
           charge = {
               'rate': 2
           }
           
       percentage= charge/100
       rate = int(amount) * percentage
       
       pay = int(amount) - rate
       
       
       if not Monify.objects.filter(reference=ref).exists():
           user = CustomUser.objects.get(account_number=acc_no, email=email)
           monify = Monify(user=user.username, reference=ref, amount=pay, status='success')
           message = f'Your deposit of {pay}naira via virtual bank transfer is successful'
           transaction= Transaction(user=user.username, service='Wallet Topup', message=message, amount=pay, amount_paid=amount, status='success', reference=ref, route='Virtual Bank', notify=True)
           user.wallet_balance += pay
           user.save()
           transaction.save()
           monify.save()
           return HttpResponse(status=200)
       
       else:
           pass



@require_POST
@csrf_exempt
def paystack_update(request):
    
    if request.method == 'POST':
       resp = json.loads(request.body)
       print(resp)
       
       status = resp['data']['status']
       ref = resp['data']['reference']
       amount = resp['data']['amount']
       address = resp['data']['ip_address']
       pay = int(amount) / 100
       print(status, ref, pay, address)
       
       
       if address == '52.31.139.75' or '52.49.173.169' or '52.214.14.220' or '213.128.80.44':
            if Paystack.objects.filter(reference=ref, status='initiated').exists():
                if not Paystack.objects.filter(reference=ref, status='success').exists():
                    print('pass')
                    paystack = Paystack.objects.get(reference=ref)
                    print(paystack.user)
                    user = CustomUser.objects.get(username=paystack.user)
                    print(user.username)
                    transaction = Transaction.objects.get(reference=ref, status='initiated')
                    if status == 'success':
                        user.wallet_balance += transaction.amount
                        paystack.status = 'success'
                        transaction.message = f'Your deposit of {transaction.amount}naira via card payment was successful'
                        transaction.status = 'success'
                        transaction.notify = True
                        transaction.beneficiary = user.username
                        transaction.amount_paid = pay
                        transaction.type = 'credit'
                        user.save()
                        transaction.save()
                        paystack.save()
                        return HttpResponse(200)
                    else:
                        pass
            
            else:
                pass
       else:
           pass



def admin(request):
    return render(request, 'dashe/admin.html')


def reset_password(request):
    return render(request, 'dash/forgot-password.html')

def reset_password_done(request):
    return render(request, 'dash/email-done.html')

def send_mail(request):
    if request.method == 'POST':
        mail = request.POST.get('mail')
        print(mail)
        
        if CustomUser.objects.filter(email=mail).exists():
            print('passedd')
            user = CustomUser.objects.get(email=mail)
            S = 15
            ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S))
            print(ran)
            
            mailer = EmailMessage(settings.CORE_NAME, f" Dear {user.username}, you are getting this mail because you have requested for a new password on your account. Kindly log in with {ran} as your temporal password and reset your password with the change password option in your dashboard.", settings.EMAIL_HOST_USER, [mail])
            mailer.fail_silently = False
            mailer.send()
            user.set_password(ran)
            user.save()
        else:
            return JsonResponse({"code": 200})  
        
    return JsonResponse({"code": 200})


