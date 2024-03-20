from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from . import models


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'total_tasks', 'undone_tasks', 'owner', 'recent_tasks']
    list_display_links = ['name']
    list_filter = ['owner']
    search_fields = ['name']
    fieldsets = (
        (None, {
            "fields": (
                'name', 'owner', 'youtube_video_hash', 'description',
            ),
        }),
    )
    autocomplete_fields = ['owner']

    def total_tasks(self, obj: models.Project):
        return obj.tasks.count()
    total_tasks.short_description = _("total tasks")

    def undone_tasks(self, obj: models.Project):
        return obj.tasks.filter(is_done=False).count()
    undone_tasks.short_description = _("undone tasks")

    def recent_tasks(self, obj: models.Project):
        return "; ".join(obj.tasks.order_by('-created_at').values_list('name', flat=True)[:3])
    recent_tasks.short_description = _("recent tasks")


class TaskAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_done', 'deadline', 'project', 'owner', 'created_at']
    list_filter = ['is_done', 'deadline', 'created_at']
    search_fields = ['name', 'description', 'project__name', 'owner__last_name', 'owner__username']
    list_editable = ['is_done', 'owner', 'project']
    readonly_fields = ['id', 'created_at', 'updated_at']
    autocomplete_fields = ['project', 'owner']
    fieldsets = (
        (_("general").title(), {
            "fields": (
                ('name', 'deadline'),
                'description', 'is_done',
            ),
        }),
        (_("ownership").title(), {
            "fields": (
                ('owner', 'project'),
            ),
        }),
        (_("temporal tracking").title(), {
            "fields": (
                ('created_at', 'updated_at', 'id'),
            ),
        }),
    )


class ProjectLikeAdmin(admin.ModelAdmin):
    list_display = ['project', 'user', 'like_type']


admin.site.register(models.Project, ProjectAdmin)
admin.site.register(models.Task, TaskAdmin)
admin.site.register(models.ProjectLike, ProjectLikeAdmin)
