from django.urls import path
from django.contrib.auth.views import LoginView

from .views import (
register_view,
logout_view,
dashboard_view,
create_account_view,
deposit_view,
withdraw_view,
transaction_history_view,
export_transactions_csv,
)

urlpatterns = [

path(
    '',
    LoginView.as_view(
        template_name='registration/login.html'
    ),
    name='home'
),

path(
    'register/',
    register_view,
    name='register'
),

path(
    'login/',
    LoginView.as_view(
        template_name='registration/login.html'
    ),
    name='login'
),

path(
    'logout/',
    logout_view,
    name='logout'
),

path(
    'dashboard/',
    dashboard_view,
    name='dashboard'
),

path(
    'account/create/',
    create_account_view,
    name='create_account'
),

path(
    'deposit/',
    deposit_view,
    name='deposit'
),

path(
    'withdraw/',
    withdraw_view,
    name='withdraw'
),

path(
    'transactions/',
    transaction_history_view,
    name='transaction_history'
),

path(
    'transactions/export/',
    export_transactions_csv,
    name='export_transactions_csv'
),

]
