from django.contrib import admin
from .models import BankAccount,Transaction

@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display=(
        'account_holder_name','account_number','current_balance','user',
    )
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display=('account','transaction_type','amount','balance_after','created_at',)
    ordering=('-created_at',)