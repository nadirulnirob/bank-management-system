import csv

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm, BankAccountForm, DepositForm,WithdrawForm
from .models import BankAccount , Transaction


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegisterForm()

    return render(
        request,
        'registration/register.html',
        {'form': form}
    )


@login_required
def dashboard_view(request):
    try:
        account = request.user.bank_account
    except BankAccount.DoesNotExist:
        account = None

    if account is None:
        return redirect('create_account')

    transactions = account.transactions.all()

    total_deposits = sum(
        transaction.amount
        for transaction in transactions
        if transaction.transaction_type == Transaction.DEPOSIT
    )

    total_withdrawals = sum(
        transaction.amount
        for transaction in transactions
        if transaction.transaction_type == Transaction.WITHDRAW
    )

    total_transactions = transactions.count()

    return render(
        request,
        'dashboard.html',
        {
            'account': account,
            'total_deposits': total_deposits,
            'total_withdrawals': total_withdrawals,
            'total_transactions': total_transactions,
        }
    )


@login_required
def create_account_view(request):
    if hasattr(request.user, 'bank_account'):
        return redirect('dashboard')

    if request.method == 'POST':
        form = BankAccountForm(request.POST)

        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()

            return redirect('dashboard')
    else:
        form = BankAccountForm()

    return render(
        request,
        'create_account.html',
        {'form': form}
    )
@login_required
def deposit_view(request):
    account = request.user.bank_account

    if request.method == 'POST':
        form = DepositForm(request.POST)

        if form.is_valid():
            amount = form.cleaned_data['amount']

            account.current_balance += amount
            account.save()

            Transaction.objects.create(
                account=account,
                transaction_type=Transaction.DEPOSIT,
                amount=amount,
                balance_after=account.current_balance
            )

            return render(
                request,
                'deposit.html',
                {
                    'form': DepositForm(),
                    'success': f'Deposit of {amount} was successful!'
                }
            )
    else:
        form = DepositForm()

    return render(
        request,
        'deposit.html',
        {'form': form}
    )

@login_required
def withdraw_view(request):
    account = request.user.bank_account

    if request.method == 'POST':
        form = WithdrawForm(request.POST)

        if form.is_valid():
            amount = form.cleaned_data['amount']

            if amount > account.current_balance:
                form.add_error(
                    'amount',
                    'Insufficient balance. You cannot withdraw more than your current balance.'
                )
            else:
                account.current_balance -= amount
                account.save()

                Transaction.objects.create(
                    account=account,
                    transaction_type=Transaction.WITHDRAW,
                    amount=amount,
                    balance_after=account.current_balance
                )

                return render(
                    request,
                    'withdraw.html',
                    {
                        'form': WithdrawForm(),
                        'success': f'Withdrawal of {amount} was successful!'
                    }
                )
    else:
        form = WithdrawForm()

    return render(
        request,
        'withdraw.html',
        {'form': form}
    )

@login_required
def transaction_history_view(request):
    account = request.user.bank_account

    transactions = account.transactions.all().order_by('-created_at')

    transaction_type = request.GET.get('type')
    date = request.GET.get('date')

    if transaction_type:
        transactions = transactions.filter(
            transaction_type=transaction_type
        )

    if date:
        transactions = transactions.filter(
            created_at__date=date
        )

    return render(
        request,
        'transaction_history.html',
        {
            'transactions': transactions,
            'selected_type': transaction_type,
            'selected_date': date,
        }
    )

@login_required
def export_transactions_csv(request):
    account = request.user.bank_account

    transactions = account.transactions.all().order_by('-created_at')

    response = HttpResponse(
        content_type='text/csv'
    )

    response['Content-Disposition'] = (
        'attachment; filename="transaction_history.csv"'
    )

    writer = csv.writer(response)

    writer.writerow([
        'Type',
        'Amount',
        'Date & Time',
        'Balance After Transaction'
    ])

    for transaction in transactions:
        writer.writerow([
            transaction.transaction_type,
            transaction.amount,
            transaction.created_at.strftime('%d %b %Y, %I:%M %p'),
            transaction.balance_after,
        ])

    return response

def logout_view(request):
    logout(request)
    return redirect('login')