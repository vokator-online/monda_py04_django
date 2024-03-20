from django.contrib import admin
from . import models


@admin.register(models.Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['subject', 'sender_name', 'sent_at', 'status']
    list_display_links = ['subject', 'sender_name']
    list_filter = ['status', 'mail_sent', 'subject', 'sent_at']
    readonly_fields = ['mail_sent', 'sent_at', 'sender_email', 'sender_name', 'mail_sent']
    fields = ['subject', 'body', 'sender_name', 'sender_email', 'sender', 'status', 'sent_at', 'mail_sent']
