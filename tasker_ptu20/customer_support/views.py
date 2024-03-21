from django.forms.models import BaseModelForm
from django.views import generic
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from . import models, forms, utils


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
        self.obj:models.Ticket = form.instance
        return super().form_valid(form)

    def get_success_url(self) -> str:
        utils.send_support_ticket_email(self.request, self.obj)
        return reverse_lazy('index')
