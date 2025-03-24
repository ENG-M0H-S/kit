from django.views.generic import TemplateView
from web_project import TemplateLayout
from django.views.generic import ListView
from auditlog.models import LogEntry
from user_sessions.models import Session
from .models import Account ,Transactions
from user_agents import parse
from django.utils import timezone
from django.http import JsonResponse
from django.shortcuts import get_object_or_404,redirect
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from decimal import Decimal
from django.contrib import messages



class UserManageView(TemplateView):
    # Predefined function
    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['log_entries'] = LogEntry.objects.all().select_related('actor')  # تحميل المستخدم مسبقًا
        context['sessions'] = Session.objects.all()
        # context['all_accounts'] = Account.objects.all()
        # context["layout_path"]

        return context

class AccountsListView(ListView):
    model = Account
    template_name = 'accounts.html'
    context_object_name = 'all_accounts'
    
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context["all_accounts"] = Account.objects.all()  # جلب الحساب الحالي فقط
        context["layout_path"]  # تأكد من تمرير القالب الأساسي
        return context

class AccountView(ListView):
    model = Account
    template_name = "myaccount.html"
    context_object_name = "accounts"

    def get_context_data(self, **kwargs):
        """إرجاع الحساب الخاص بالمستخدم وإضافة بيانات إضافية"""
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context["accounts"] = Account.objects.filter(user=self.request.user)  # جلب الحساب الحالي فقط
        context["layout_path"]  # تأكد من تمرير القالب الأساسي
        return context


class AuditLogView(ListView):
    model = LogEntry
    template_name = 'auditlog.html'
    context_object_name = 'log_entries'

class SessionsView(ListView):
    model = Session
    template_name = 'sessions.html'
    context_object_name = 'sessions'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        sessions_with_parsed_ua = []

        for session in context['sessions']:
            session.is_valid = session.expire_date > timezone.now()
            if session.user_agent:  # تحقق من وجود user_agent
                user_agent = parse(session.user_agent)
                session.browser = user_agent.browser.family  # المتصفح (مثل Edge, Chrome)
                session.os = user_agent.os.family  # نظام التشغيل (مثل Windows 10, macOS)
                session.device = f"{session.browser} on {session.os}"  # الجهاز بشكل مقروء
            else:
                session.browser = "Unknown Browser"
                session.os = "Unknown OS"
                session.device = "Unknown Device"

            sessions_with_parsed_ua.append(session)

        context['sessions'] = sessions_with_parsed_ua
        return context



def Add_Balance(request, account_id):
    account = get_object_or_404(Account, id=account_id)

    if account.status == "inactive":
        messages.error(request, "لا يمكن الإيداع في حساب غير مفعل.")
        return redirect("accounts")

    if request.method == "POST":
        amount = request.POST.get("amount")

        try:
            amount = Decimal(amount)  # تحويل المبلغ إلى Decimal
        except:
            messages.error(request, "يجب إدخال مبلغ صحيح.")
            return redirect("accounts")

        if amount <= 0:
            messages.error(request, "يجب إدخال مبلغ صحيح.")
            return redirect("accounts")

        with transaction.atomic():
            account.balance += amount
            account.save()

            Transactions.objects.create(
                account=account,
                transaction_type="deposit",
                amount=amount,
                # created_by=request.user
            )

        messages.success(request, f"تم إيداع {amount}$ بنجاح في الحساب {account.account_number}.")
        return redirect("accounts")

    return redirect("accounts")


def Withdraw_balance(request, account_id):
    account = get_object_or_404(Account, id=account_id)

    if account.status == "inactive":
        messages.error(request, "لا يمكن السحب من حساب غير مفعل.")
        return redirect("accounts")

    if request.method == "POST":
        amount = request.POST.get("amount")
        if not amount or Decimal(amount) <= 0:  # ✅ استخدام Decimal
            messages.error(request, "يجب إدخال مبلغ صحيح.")
            return redirect("accounts")

        if Decimal(amount) > account.balance:  # ✅ التأكد من الرصيد باستخدام Decimal
            messages.error(request, "الرصيد غير كافٍ لإتمام السحب.")
            return redirect("accounts")

        with transaction.atomic():
            account.balance -= Decimal(amount)  # ✅ تحويل `amount` إلى Decimal
            account.save()

            Transactions.objects.create(
                account=account,
                transaction_type="withdraw",
                amount=Decimal(amount),  # ✅ تأكد أن الحقل يخزن قيمة Decimal
            )

        messages.success(request, f"تم سحب {amount}$ بنجاح من الحساب {account.account_number}.")
        return redirect("accounts")

    return redirect("accounts")

def Add_Transaction(account, amount, transaction_type, description=None):
    Transactions.objects.create(
        account = account,
        amount = amount,
        transaction_type = transaction_type,
        description = description,
        transaction_date =now()
    )
   
def toggle_account_status(request, account_id):
    account = get_object_or_404(Account, id=account_id)
    
    # التبديل بين "active" و "inactive"
    account.status = "inactive" if account.status == "active" else "active"
    account.save()
    
    status = "مفعل" if account.status == "active" else "معطل"
    messages.success(request, f"تم تغيير حالة الحساب إلى {status}.")
    
    return redirect('accounts')