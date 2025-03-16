from django.views.generic import TemplateView
from web_project import TemplateLayout
from django.views.generic import ListView
from auditlog.models import LogEntry
from user_sessions.models import Session
from user_agents import parse
from django.utils import timezone

class UserManageView(TemplateView):
    # Predefined function
    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['log_entries'] = LogEntry.objects.all().select_related('actor')  # تحميل المستخدم مسبقًا
        context['sessions'] = Session.objects.all()

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