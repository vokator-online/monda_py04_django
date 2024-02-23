from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _
from tinymce.models import HTMLField


class Project(models.Model):
    name = models.CharField(_("name"), max_length=100, db_index=True)
    owner = models.ForeignKey(
        get_user_model(), 
        verbose_name=_("owner"), 
        on_delete=models.CASCADE,
        related_name='projects',
    )
    description = HTMLField(max_length=10000, null=True, blank=True)
    youtube_video_hash = models.CharField(
        _("YouTube video hash"), 
        max_length=50, 
        null=True, blank=True,
        help_text=_("from Youtube's video URL copy the part after 'https://www.youtube.com/watch?v='.")
    )

    class Meta:
        verbose_name = _("project")
        verbose_name_plural = _("projects")
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("project_detail", kwargs={"pk": self.pk})


class Task(models.Model):
    name = models.CharField(_("name"), max_length=100, db_index=True)
    description = HTMLField(max_length=10000, null=True, blank=True)
    project = models.ForeignKey(
        Project,
        verbose_name=_("project"), 
        on_delete=models.CASCADE,
        related_name='tasks',
    )
    owner = models.ForeignKey(
        get_user_model(), 
        verbose_name=_("owner"), 
        on_delete=models.CASCADE,
        related_name='tasks'
    )
    created_at = models.DateTimeField(_("created at"), auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True, db_index=True)
    is_done = models.BooleanField(_("is done"), default=False, db_index=True)
    deadline = models.DateTimeField(_("deadline"), null=True, blank=True, db_index=True)

    class Meta:
        verbose_name = _("task")
        verbose_name_plural = _("tasks")
        ordering = ['is_done', '-created_at']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("task_detail", kwargs={"pk": self.pk})


class ProjectLike(models.Model):
    project = models.ForeignKey(
        Project, 
        verbose_name=_("project"), 
        on_delete=models.CASCADE,
        related_name='likes',
    )
    user = models.ForeignKey(
        get_user_model(), 
        verbose_name=_("user"), 
        on_delete=models.CASCADE,
        related_name='project_likes',
    )

    class Meta:
        verbose_name = _("project like")
        verbose_name_plural = _("project likes")

    def __str__(self):
        return f"{self.project} {self.user}"

    def get_absolute_url(self):
        return reverse("project_like_detail", kwargs={"pk": self.pk})
