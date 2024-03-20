from typing import Iterable
from django.db import models
from django.utils.translation import gettext as _
from django.urls import reverse
from django.contrib.auth import get_user_model


SUBJECT_CHOICES = (
    ('billing', _('billing and payments')),
    ('bugs', _('report a bug')),
    ('contact', _('contact request')),
    ('other', _('everything else')),
)

TICKET_STATUSES = (
    ('new', _('new')),
    ('read', _('read')),
    ('processing', _('processing')),
    ('closed', _('closed')),
)


class Ticket(models.Model):
    subject = models.CharField(_("subject"), max_length=50, choices=SUBJECT_CHOICES, default='other')
    body = models.TextField(_("body"), max_length=10000, default='', blank=True)
    sender = models.ForeignKey(
        get_user_model(), 
        verbose_name=_("sender"), 
        on_delete=models.CASCADE, 
        related_name='support_tickets', 
        null=True, blank=True,
    )
    sender_name = models.CharField(_("full name"), max_length=100, null=True, blank=True)
    sender_email = models.EmailField(_("email"), max_length=254, null=True, blank=True)
    sent_at = models.DateTimeField(_("sent at"), auto_now_add=True, db_index=True)
    mail_sent = models.BooleanField(_("email sent"), default=False)
    status = models.CharField(_("status"), max_length=15, choices=TICKET_STATUSES, default='new', db_index=True)

    class Meta:
        verbose_name = _("ticket")
        verbose_name_plural = _("tickets")
        ordering = ['-sent_at']

    def __str__(self):
        return _("{} from {} sent {}").format(
            self.subject,
            self.sender_email,
            self.sent_at,
        )

    def clean(self) -> None:
        if self.sender:
            self.sender_email = self.sender.email
            self.sender_name = f"{self.sender.first_name} {self.sender.last_name}"

    def get_absolute_url(self):
        return reverse("ticket_detail", kwargs={"pk": self.pk})
