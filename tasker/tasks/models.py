from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model


class Project(models.Model):
    name = models.CharField(_("name"), max_length=100, db_index=True)
    owner = models.ForeignKey(
        get_user_model(), 
        on_delete=models.CASCADE, 
        verbose_name=_("owner"), 
        related_name='projects',
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("project")
        verbose_name_plural = _("projects")
        ordering = ['name']


class Task(models.Model):
    name = models.CharField(_("name"), max_length=100, db_index=True)
    description = models.TextField(_("description"), blank=True, max_length=10000)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE, 
        verbose_name=_("project"), 
        related_name='tasks',
    )
    owner = models.ForeignKey(
        get_user_model(), 
        on_delete=models.CASCADE, 
        verbose_name=_("owner"), 
        related_name='tasks',
    )
    created_at = models.DateTimeField(_("created at"), auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True, db_index=True)
    is_done = models.BooleanField(_("is done"), default=False, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("task")
        verbose_name_plural = _("tasks")
        ordering = ['is_done', '-created_at']
