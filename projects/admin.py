from django.contrib import admin
from .models import GitHubDataSource, Project, Task


@admin.register(GitHubDataSource)
class GitHubDataSourceAdmin(admin.ModelAdmin):
    pass


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    pass


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    pass
