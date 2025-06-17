from django.contrib import admin
from .models import *
import random
import uuid
from datetime import datetime
from datetime import date


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'name', 'phone_no', 'email', 'package', 'total_referal', 'wallet_balance', 'referal_bonus', 'bank_name', 'account_number', 'account_name')
    search_fields = ('username','email','phone_no',)
    

class DataNetworkAdmin(admin.ModelAdmin):
    list_display = ('name', 'network_id', 'is_active')
    
class DataPlanTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'network', 'is_available')
    
class DataPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'network', 'plan_type', 'plan_id', 'silver_price', 'gold_price', 'diamond_price', 'is_active')
    search_fields = ('name', 'network', 'plan_type')
    
class DecoderAdmin(admin.ModelAdmin):
    list_display = ('name', 'provider_id', 'is_active')
    
class CablePlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'decoder', 'plan_id', 'silver_price', 'gold_price', 'diamond_price', 'is_active')
    search_fields = ('name', 'decoder')
    
class DiscoAdmin(admin.ModelAdmin):
    list_display = ('name', 'disco_type' 'disco_id', 'silver_convinience_fee', 'gold_convinience_fee', 'diamond_convinience_fee', 'is_active')
    
    
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'service', 'plan', 'amount', 'amount_paid', 'date_ordered', 'reference', 'status', 'beneficiary', 'beneficiary_name', 'type', 'route')
    search_fields = ('user','service','reference', 'beneficiary')
    
    #fields = ['user', 'amount_paid', 'status']
    
    actions = ['reverse_transaction']
    
    #def queryset(self, request):
     #   qs = Transaction.objects.get(reference=self.reference)
      #  return qs
    
    
    @admin.action(description='Reverse Selected Transactions')
    def reverse_transaction(self, request, queryset):
        
        print(self)
        print(request)
        print(queryset)
        
        qs = queryset
        for q in qs:
            print(q.id)
        
            tran = Transaction.objects.get(id=q.id)
            print(tran)
            time = datetime.today().strftime("%Y%m%d%H%M")
            def create_id():
                num = random.randint(1, 10)
                num_2 = random.randint(1, 10)
                num_3 = random.randint(1, 10)
                return str(num_3)+str(num_2)+str(uuid.uuid4())[:6]

            ident = time + create_id()
        
        
            while Transaction.objects.filter(reference = ident).exists():
                ident = create_id()
                
            if tran.status != 'failed':
                if tran.status != 'reversed':
                    if tran.service != 'Reversal':
                        if tran.service != 'Wallet Topup':
                            if tran.service != 'Wallet Debit':
                                user = CustomUser.objects.get(username=q.user)
                                print(user)
                                user.wallet_balance += tran.amount_paid
                                tran.status = 'reversed'
                                tran.save()
                                user.save()
                                msg = f'{tran.amount_paid}naira was successfully reversed for failed transaction - ({tran.service})'
                                new_tran = Transaction(user=user.username, service='Reversal', plan='Reversed Transaction', message=msg, amount=tran.amount_paid, type='credit', amount_paid=tran.amount_paid, status='success', reference=ident, notify=True, bal_after=user.wallet_balance, bal_before=(user.wallet_balance - tran.amount_paid))
                                new_tran.save()
                            else:
                                pass
                        else:
                            pass
                    else:
                        pass
                else:
                    print('Transaction Already Reversed') 
            else:
                print('Transaction Failed Already')
        #queryset.update(status='reversed')    
        
class ReferralAdmin(admin.ModelAdmin):
    list_display = ('referrer', 'referred')
    
class ReferralBonusAdmin(admin.ModelAdmin):
    list_display = ('bonus', 'per_transaction', 'per_upgrade')
    
class AirtimeNetworkAdmin(admin.ModelAdmin):
    list_display=('name', 'network_id', 'is_available')
    
#class AirtimeTypeAdmin(admin.ModelAdmin):
 #   list_display= ('network', 'name', 'type_id', 'is_available')
    
class AirtimeAdmin(admin.ModelAdmin):
    list_display = ('network', 'types', 'silver_rate', 'gold_rate', 'diamond_rate', 'is_available')
    
    
class PaystackAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'reference', 'date_ordered', 'status')
    search_fields = ('user', 'reference')
    
    
class MonifyAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'reference', 'date_ordered', 'status')
    search_fields = ('user', 'reference')
    
    
class MonifyRateAdmin(admin.ModelAdmin):
    list_display = ('name', 'rate')
    
class MessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'message')
    
class UpgradePriceAdmin(admin.ModelAdmin):
    list_display = ('name', 'agent')
    
    
class WalletActionAdmin(admin.ModelAdmin):
    list_display= ('username', 'action', 'amount')
    #fields = ['user', 'amount']
    #actions = ['credit', 'debit']
    
    
class ManualBankAdmin(admin.ModelAdmin):
    list_display= ('bank_name', 'acc_name', 'acc_no')
    



admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(DataNetwork, DataNetworkAdmin)
admin.site.register(DataPlanType, DataPlanTypeAdmin)
admin.site.register(DataPlan, DataPlanAdmin)
admin.site.register(Decoder, DecoderAdmin)
admin.site.register(CablePlan, CablePlanAdmin)
admin.site.register(Disco)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Referral, ReferralAdmin)
admin.site.register(ReferralBonus, ReferralBonusAdmin)
admin.site.register(Airtime, AirtimeAdmin)
admin.site.register(AirtimeNetwork, AirtimeNetworkAdmin)
admin.site.register(Paystack, PaystackAdmin)
admin.site.register(Monify, MonifyAdmin)
admin.site.register(MonifyRate, MonifyRateAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(UpgradePrice, UpgradePriceAdmin)
admin.site.register(WalletAction, WalletActionAdmin)
admin.site.register(ManualBank, ManualBankAdmin)
