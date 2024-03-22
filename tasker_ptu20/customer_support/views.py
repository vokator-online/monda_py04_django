from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.views import generic
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from . import models, forms, utils


class TicketList(LoginRequiredMixin, generic.ListView):
    model = models.Ticket
    template_name = 'customer_support/ticket_list.html'

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()
        qs = qs.filter(sender=self.request.user)
        return qs


class TicketDetail(UserPassesTestMixin, generic.DetailView):
    model = models.Ticket
    template_name = 'customer_support/ticket_detail.html'

    def test_func(self) -> bool | None:
        obj = self.get_object()
        if self.request.user.is_authenticated:
            if obj.sender == self.request.user:
                return True
        else:
            if not obj.sender:
                return True
        return False


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
