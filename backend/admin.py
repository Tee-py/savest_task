from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from .models import UserMetrics
from .functions import *
from .forms import MailForm
from django.urls import path
from django.urls import reverse
from django.core.mail import send_mail
from django.template.response import TemplateResponse

# Register your models here.

class UserAdmin(admin.ModelAdmin):

    list_display = ['username', 'email', 'first_name', 'last_name', 'is_active', 'last_login', 'user_actions']
    change_list_template = 'admin/userlist.html'
    list_filter = ('is_staff', 'is_active')
    search_fields = ['username']

    def get_urls(self): 
        #calls the super classes's get_urls() method
        urls = super().get_urls()
        #urls for activating and deactivating user
        custom_urs = [
            path(
                '<int:pk>/activate-account', 
                self.admin_site.admin_view(self.activate),
                name='activate-account'
            ),
            path(
                '<int:pk>/deactivate-account',
                self.admin_site.admin_view(self.deactivate),
                name='deactivate-account'
            ),
            path(
                'send_bulk_mail',
                self.admin_site.admin_view(self.send_mail_to_users),
                name='send_mail'
            )
        ]
        #return the custom url and the super classes's url
        return custom_urs + urls

    def activate(self, request, pk, *args, **kwargs):
        """
        Method to activate user account
        """
        user = self.get_object(request, pk)
        user.is_active = True
        user.save()
        self.message_user(request, 'User {} activated successfully'.format(user.username))
        return HttpResponseRedirect('/admin/auth/user')

    def deactivate(self, request, pk, *args, **kwargs):
        """
        Method to deactivate user account
        """
        user = self.get_object(request, pk)
        user.is_active = False
        user.save()
        self.message_user(request, 'User {} deactivated successfully'.format(user.username)) 
        return HttpResponseRedirect('/admin/auth/user')

    def send_mail_to_users(self, request):
        if request.method == "GET":
            form = MailForm()
            return TemplateResponse(request, 'admin/mailform.html', {'form':form})
        else:
            form = MailForm(request.POST)
            if form.is_valid():
                all_mails = [user.email for user in User.objects.all() if user.is_superuser==False and user.is_active==True]
                form_data = form.clean()
                try:
                    send_mail(
                        form_data['subject'],
                        form_data['body'],
                        form_data['From'],
                        all_mails,
                        fail_silently = False
                    )
                    self.message_user(request, 'Mail sent succesfully')
                    return HttpResponseRedirect('/admin/auth/user')
                except:
                    self.message_user(request, 'Mail was not successful')
                    return HttpResponseRedirect('/admin/auth/user')
            else:
                return TemplateResponse(request, 'admin/mailform.html', {'form':form})

    def user_actions(self, obj):
        """
        Method to display buttons for activating and deactivating 
        a user account
        """
        return format_html(
            '<a class="button" href={}>Acitvate</a>&nbsp;'
            '<a class="button" href={}>Deactivate</a>',
            reverse('admin:activate-account', args=[obj.pk]),
            reverse('admin:deactivate-account', args=[obj.pk]),
        )
    
    user_actions.short_description = 'User Actions'
    user_actions.allow_tags = True


class UserMetricsAdmin(admin.ModelAdmin):
    change_list_template = "admin/metrics.html"

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)
        metrics = [
            {'value': grab_active_users(User), 'Title': 'Active Users'},
            {'value': grab_total_users(User), 'Title': 'Total Users'},
            {'value': grab_registered_users(User, interval='day'), 'Title': 'Registered users in the past 24hrs'},
            {'value': grab_registered_users(User, interval='week'), 'Title': 'Registered users in the past Week'},
            {'value': grab_registered_users(User, interval='month'), 'Title': 'Registered users in the past Month'}
        ]
        response.context_data['metrics'] = metrics
        return response


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(UserMetrics, UserMetricsAdmin)