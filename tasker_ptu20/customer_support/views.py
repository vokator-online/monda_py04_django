from django.forms.models import BaseModelForm
from django.shortcuts import render
from django.views import generic
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.urls import reverse_lazy
from django.template.loader import get_template
from django.core.mail import send_mail
from . import models, forms


class TicketCreateView(generic.CreateView):
    model = models.Ticket
    template_name = 'customer_support/ticket_create.html'

    def get_form_class(self) -> type[BaseModelForm]:
        if self.request.user.is_authenticated:
            return forms.TicketFormUser
        else:
            return forms.TicketFormGuest

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.sender = self.request.user
            form.instance.clean()
        self.object:models.Ticket = form.instance
        return super().form_valid(form)

    def get_success_url(self) -> str:
        template_text = get_template('customer_support/ticket_email_text.html')
        message = template_text.render({'obj': self.object})
        try:
            send_mail(f"Support Ticket: {self.object.subject}", message, self.object.sender_email, ["kestas@midonow.fi"])
        except Exception as error:
            messages.warning(self.request, _("Thank you. We had some issues ({}) but we still got your message.").format(error))
        else:
            self.object.mail_sent = True
            self.object.save()
            messages.success(self.request, _("Thank you. We will get back to you as soon as we can."))
        return reverse_lazy('index')
