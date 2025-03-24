from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path(
        "",
        login_required(UserManageView.as_view(template_name="index.html")),
        name="index",
    ),
    path(
        "page_2/",
        login_required(UserManageView.as_view(template_name="page_2.html")),
        name="page-2",
    ),
    path(
        "auditlog/", 
        login_required(UserManageView.as_view(template_name="auditlog.html")), 
        name="auditlog"
        ),
    path(
        "sessions/", 
        login_required(SessionsView.as_view(template_name="sessions.html")), 
        name="sessions"
        ),
    path(
        "myaccount/", 
        login_required(AccountView.as_view(template_name="myaccount.html")), 
        name="myaccount"
        ),
    path(
        "accounts/", 
        login_required(AccountsListView.as_view(template_name="accounts.html")), 
        name="accounts"
        ),
    
    path('accounts/deposit/<int:account_id>/', Add_Balance, name='deposit'),
    path('accounts/withdraw/<int:account_id>/', Withdraw_balance, name='withdraw'),
    path('accounts/toggle-status/<int:account_id>/', toggle_account_status, name='toggle_account_status'),
]
