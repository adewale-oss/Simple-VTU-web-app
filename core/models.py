from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.base import Model
from django.conf import settings
from django.http import *
from django.core.exceptions import *
import random
import uuid
from datetime import datetime
from datetime import date


class LoggedInUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='logged_in_user', on_delete=models.CASCADE)
    session_key = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.user.username


class DataNetwork(models.Model):
    name = models.CharField(max_length=200, null=False)
    network_id = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    

class DataPlanType(models.Model):
    
    TYPES = (
        ('CORPORATE GIFTING', 'CORPORATE GIFTING'),
        ('GIFTING', 'GIFTING'),
        ('SME', 'SME')
    )
    
    name = models.CharField(choices=TYPES, default='SME', max_length=200)
    network = models.ForeignKey(DataNetwork, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=False)
    
    def __str__(self):
        return self.network.name + ' ' + self.name
    
    
class DataPlan(models.Model):
    name = models.CharField(max_length=500, null=False)
    network = models.ForeignKey(DataNetwork, on_delete=models.CASCADE)
    plan_type = models.ForeignKey(DataPlanType, on_delete=models.CASCADE)
    plan_id = models.CharField(max_length=100)
    silver_price = models.FloatField(null=False)
    gold_price = models.FloatField(null=False)
    diamond_price = models.FloatField(null=False)
    is_active = models.BooleanField(default=False)
    
    
    def __str__(self):
        return self.name

class AirtimeNetwork(models.Model):
    name = models.CharField(max_length=50)
    network_id = models.CharField(max_length=50)
    is_available = models.BooleanField(default=False)
    
    
    def __str__(self):
        return self.name
    
  
class Airtime(models.Model):
    
    types = (
        ('VTU', 'VTU'),
        ('SNS', 'SNS'),
    )
    
    network = models.ForeignKey(AirtimeNetwork, on_delete=models.CASCADE)
    types = models.CharField(choices=types, default='VTU', max_length=100)
    plan_id = models.CharField(null=True, blank=True, max_length=100)
    silver_rate = models.FloatField(null=False, default=100)
    gold_rate = models.FloatField(null=False, default=100)
    diamond_rate = models.FloatField(null=False, default=100)
    is_available = models.BooleanField(default=False)
    
    def __str__(self):
        return self.network.name + ' ' +self.types
    
    
    

    
class Decoder(models.Model):
    name = models.CharField(max_length=100, null=False)
    provider_id = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    
    
class CablePlan(models.Model):
    name = models.CharField(max_length=500, null=False)
    decoder = models.ForeignKey(Decoder, on_delete=models.CASCADE)
    plan_id = models.CharField(max_length=100)
    silver_price = models.FloatField(null=False)
    gold_price = models.FloatField(null=False)
    diamond_price = models.FloatField(null=False)
    is_active = models.BooleanField(default=False)
    
    
    def __str__(self):
        return self.name
      

class CustomUser(AbstractUser):
    
    PACKAGES = (
        ('Silver', 'Silver'),
        ('Gold', 'Gold'),
        ('Diamond', 'Diamond')
         
    )
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=150)
    phone_no = models.CharField(max_length=20)
    package = models.CharField(choices= PACKAGES, max_length=20, default='Silver')
    wallet_balance = models.FloatField(default='0')
    referal_bonus = models.FloatField(default='0')
    total_referal = models.IntegerField(default='0')
    account_number = models.CharField(max_length=15, default='0')
    account_name = models.CharField(max_length=200, default='user')
    bank_name = models.CharField(max_length=50, default='bank')
    account_ref = models.CharField(max_length=100, default='ref')
    pin = models.CharField(max_length=10, blank=True, null=True)
    
    
    def __str__(self):
        return self.username
    
    
    def clean_first_name(self):
        self.first_name = self.cleaned_data['first_name']
        self.first_name= first_name[0].upper() + first_name[1:].lower()
        return super(CustomUser, self).save(*args, kwargs)
    
    def clean_last_name(self):
        self.last_name = self.cleaned_data['last_name']
        self.last_name= last_name[0].upper() + last_name[1:].lower()
        return super(CustomUser, self).save(*args, kwargs)

    
    def clean_username(self):
        self.username = self.cleaned_data['username']
        return super(CustomUser, self).save(*args, kwargs)
    
    def clean_email(self):
        self.email = self.cleaned_data['email']
        return super(CustomUser, self).save(*args, kwargs)
    
    def clean_phone_no(self):
        self.phone_no = self.cleaned_data['phone_no']
        return super(CustomUser, self).save(*args, kwargs)
    
    
    

    
    
    
class Disco(models.Model):
    
    TYPE = (
        ('PREPAID', 'PREPAID'),
        ('POSTPAID', 'POSTPAID')
    )
    name = models.CharField(max_length=200)
    type = models.CharField(choices=TYPE, default='PREPAID', max_length=100)
    disco_id = models.CharField(max_length=20)
    silver_convinience_fee = models.FloatField(null=False)
    gold_convinience_fee = models.FloatField(null=False)
    diamond_convinience_fee = models.FloatField(null=False)
    is_active = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name + ' ' + self.type
    
   
    
class EPin(models.Model):
    name = models.CharField(max_length=200)
    end_user_price = models.IntegerField()
    smart_earner_price = models.IntegerField()
    top_user_price = models.IntegerField()
    is_available = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    
    
class CardPinNetwork(models.Model):
    name= models.CharField(max_length=100)
    is_available = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    
    
class CardPin(models.Model):
    network = models.ForeignKey(CardPinNetwork, on_delete=models.CASCADE)
    default_price = models.CharField(max_length=200)
    end_user_discount = models.IntegerField()
    smart_earner_discount = models.IntegerField()
    top_user_discount = models.IntegerField()
    is_available = models.BooleanField(default=False)
    
    def __str__(self):
        return self.default_price
    
    
class Transaction(models.Model):
    
    STATUS = (
        ('success', 'success'),
        ('pending', 'pending'),
        ('initiated', 'initiated'), 
        ('failed', 'failed'),
        ('reversed', 'reversed')
    )
    
    TYPE = (
        ('debit', 'debit'),
        ('credit', 'credit')
    )
    
    
    user = models.CharField(max_length=100)
    service = models.CharField(max_length=100)
    plan = models.CharField(max_length=200, null=True, blank=True)
    amount = models.FloatField(null=True, blank=True)
    amount_paid = models.FloatField(null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS, max_length=40, default='initiated')
    reference = models.CharField(max_length=500, blank=True, null=True)
    message = models.CharField(max_length=500, blank=True, null=True)
    beneficiary = models.CharField(max_length=200, null=True, blank=True)
    beneficiary_name = models.CharField(max_length=200, blank=True, null=True)
    type = models.CharField(choices=TYPE, max_length=100, default='debit')
    notify = models.BooleanField(default=False)
    route = models.CharField(max_length=200, null=True, blank=True)
    bal_before = models.FloatField(null=True, blank=True)
    bal_after = models.FloatField(null=True, blank=True)
    topic = models.CharField(max_length=200, default='Payment Recieved')
    convinience_fee = models.FloatField(null=True, blank=True)
    token = models.CharField(max_length=500, null=True, blank=True)
    
    #def __int__(self):
     #   return self.id
    

class Paystack(models.Model):
    
    STATUS = (
        ('success', 'success'),
        ('pending', 'pending'),
        ('failed', 'failed'),
        ('initiated', 'initiated'),
    )
    
    user = models.CharField(max_length=400, default='user')
    amount = models.IntegerField()
    reference = models.CharField(max_length=500)
    status = models.CharField(choices=STATUS, max_length=40, default='initiated')
    date_ordered = models.DateTimeField(auto_now_add=True)
    
    
class PaystackCharge(models.Model):
    name = models.CharField(max_length=20, default='charge', unique=True)
    rate = models.IntegerField(default=2)
    
    
class Monify(models.Model):
    STATUS = (
        ('success', 'success'),
        ('pending', 'pending'),
        ('failed', 'failed')
    )
    
    user = models.CharField(max_length=100)
    amount = models.IntegerField()
    reference = models.CharField(max_length=500)
    status = models.CharField(choices=STATUS, max_length=40, default='pending')
    date_ordered = models.DateTimeField(auto_now_add=True)
    
    
class MonifyRate(models.Model):
    name = models.CharField(max_length=100, default='rate', unique=True)
    rate = models.FloatField(null=False)


class Referral(models.Model):
    referrer = models.CharField(max_length=100,)
    referred = models.CharField(max_length=100)
    
    
class ReferralBonus(models.Model):
    bonus = models.CharField(max_length=100, default='ref_bonus', unique=True)
    per_transaction = models.IntegerField()
    per_upgrade = models.IntegerField()



class Message(models.Model):
    name = models.CharField(max_length=100, default='message', unique=True)
    message = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name
        
        
class UpgradePrice(models.Model):
    name = models.CharField(max_length=30, default='price', unique=True)
    agent = models.IntegerField()
    def __str__(self):
        return self.name
    

class ManualBank(models.Model):
    name = models.CharField(max_length=50, default='bank', unique=True)
    bank_name = models.CharField(max_length=50)
    acc_no = models.CharField(max_length=20)
    acc_name = models.CharField(max_length=50)
    
    
class WalletAction(models.Model):
    
    ACTIONS = (
        ('CREDIT', 'CREDIT'),
        ('DEBIT', 'DEBIT')
    )
    
    username = models.CharField(max_length=200)
    action = models.CharField(choices=ACTIONS, max_length=100)
    amount = models.FloatField()
    
    def __str__(self):
        return self.username
    
    
    
    def save(self, *args, **kwargs):
        time = datetime.today().strftime("%Y%m%d%H%M")
        def create_id():
            num = random.randint(1, 10)
            num_2 = random.randint(1, 10)
            num_3 = random.randint(1, 10)
            return str(num_3)+str(num_2)+str(uuid.uuid4())[:6]

        ident = time + create_id()
        
        
        while Transaction.objects.filter(reference = ident).exists():
            ident = create_id()
            
            
        try:
            user = CustomUser.objects.get(username=self.username)
        except CustomUser.DoesNotExist:
            return HttpResponse('Error: Username Not Found')
        #return HttpResponse(user)

        if self.action == 'CREDIT':
            user.wallet_balance += self.amount
            user.save()
            msg = f'Your deposit of {self.amount}naira via admin load is successful'
            t= Transaction(user=user.username, service='Wallet Topup', plan='Manual Funding', message=msg, amount=self.amount, route='Admin', type='credit', amount_paid=self.amount, status='success', reference=ident, notify=True)
            t.save()
        else:
            user.wallet_balance -= self.amount
            user.save()
            msg = f"{self.amount}naira has been debited from your account. Contact admin if you don't know why"
            tr= Transaction(user=user.username, service='Wallet Debit', plan='Manual Debit', topic='Wallet Debited', message=msg, amount=self.amount, route='Admin', type='debit', status='success', reference=ident, notify=True)
            tr.save()
        super(WalletAction, self).save(*args, **kwargs)
    
    
